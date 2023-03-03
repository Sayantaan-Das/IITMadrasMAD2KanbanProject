<template>

    
        <div class="col-sm-6 col-md-4 col-xl-3 py-3 px-3">
            <div class="card bg-light">
                <div class="card-body">
                    <h6 class="card-title text-uppercase text-truncate py-2"> {{ this.taskName }}</h6>
                    <p> {{ this.taskDesc }}</p>
                    

                  <div class="btn-group py-2">
                    <button class="btn btn-outline-success" v-on:click="addCard()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>
                      </svg>
                    </button>

                    <button class="btn btn-outline-success"  v-on:click="editTaskList()">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                          <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                          <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                       </svg>
                      </button>

                    <button class="btn btn-outline-danger" v-on:click="confirmDeleteTask()">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                        <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
                      </svg>
                    </button>
                    <br>
                  </div>
                  <br>
                  <div class="items border border-light">
                        
                            <div class="container-fluid" v-if='cardlist'>
    
                                <CardViewVue v-for='cards in cardlist'
                                :key='cards.id'
                                :card='cards'
                                @CardUpdated="reloadTaskList()"
                                />
                            
                            </div>
                  <div class="card shadow-sm"></div>
                  </div>
                </div>
            </div>
        </div>


</template>

<script>

import CardViewVue from './CardView.vue';

export default{
    name: 'TaskList',
    data(){
        return{
            
            cardlist: [],
            modal: false
            

        }
    },

    props: ['task','taskName','taskDesc'],

    components: {
        CardViewVue
    },


    methods: {

      setID(){
           localStorage.setItem("Task-Id",this.task);
           localStorage.setItem("Task-Title",this.taskName);
           localStorage.setItem("Task-Description",this.taskDesc);
      },
      remID(){
            if(localStorage.getItem("Task-Id")){
                localStorage.removeItem("Task-Id");
           localStorage.removeItem("Task-Title");
           localStorage.removeItem("Card-Description");
          
            }
        },



        reloadTaskList(){
          console.log("reload runnng");
          fetch("http://localhost:8000/api/card/"+this.task, {
            method: 'GET',
      headers: {
        'Authentication-Token': localStorage.getItem('Authentication-Token')
        }})
        .then(function(response){ if(response.status==200){ return response.json();} else{ return null;}})
        .then(response => this.cardlist= response);

        },
        addCard: function() {
          this.setID();
          this.$router.push({ path: '/newcard' })
         

        },

        editTaskList: function(){
          this.setID();
          this.$router.push({ path: '/edittasklist' });
        },

       async confirmDeleteTask(){
        if(  confirm("Are you sure you want to delete the Task List?\nAll its associated Cards would also get deleted.\nYou won't be able to recover them once deleted! Consider moving the Cards to any other Task List!"))
        {
            const response=await fetch("http://localhost:8000/api/task/"+this.task, {
            method: 'DELETE',
      headers: {
        'Authentication-Token': localStorage.getItem('Authentication-Token')
        }});
       if(response.status==200){
        this.$emit("taskUpdated");}
        
        }},

     

     }, 

    mounted(){
        fetch("http://localhost:8000/api/card/"+this.task, {
            method: 'GET',
      headers: {
        'Authentication-Token': localStorage.getItem('Authentication-Token')
        }})
        .then(function(response){ if(response.status==200){ return response.json();} else{ return null;}})
        .then(response => {this.cardlist= response;});
       
     }
}


</script>