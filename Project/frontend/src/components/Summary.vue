<template>

  <div class="row">
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
      <div class="container-fluid">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link active">Welcome {{user_name}}</a>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item justify-content-end">
            <a class="nav-link" v-on:click="this.$router.push({ path: '/logout' })">Logout</a>
          </li>
        </ul>
      </div>
    </nav>
</div>

<div class="row">
  <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <div class="container-fluid">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active">Placeholder</a>
        </li>
      </ul>
    </div>
  </nav>
</div>

<ul class="nav nav-tabs">
  <li class="nav-item">
    <a class="nav-link" v-on:click="this.$router.push({ path: '/board' })">Kanban Board</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" v-on:click="this.$router.push({ path: '/newtasklist' })">Create New Task List</a>
  </li>
  <li class="nav-item">
    <a class="nav-link active">Summary</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" v-on:click="this.$router.push({ path: '/profile' })">Profile</a>
  </li>
</ul>
<br>

<div class="container-fluid">
  <div class="btn-group">
  <button class="btn btn-outline-success" v-on:click="taskListReport()">Get a CSV Task List Report via e-mail</button>
  <button class="btn btn-outline-success" v-on:click="getAllSelectedCardsReport()">Get Cards reports for all selected Task Lists</button>
  </div>
</div>

<br>

<div class="container-fluid">
<div class="table-responsive">
    <table class="table table-bordered">
        <thead class="table-dark">
            <tr>
                <th scope="col">  </th>
                <th scope="col">Task List Title</th>
                <th scope="col">Task List Description</th>
                <th scope="col">Number of Cards in the Task List</th>
                <th scope="col">Number of Cards Completed</th>
                <th scope="col">Number of Cards Incomplete</th>
                <th scope="col">Number of Incomplete Cards with overdue Deadline</th>
                <th scope="col">Number of Cards completed within Deadline</th>
                <th scope="col">Action</th>
            </tr>
        </thead>
          <tbody v-for='summary in this.summary_response' id="tab" :key="summary.id">
            <tr>
              <td>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" name="check" v-model="checked_list" :value="summary.id" >
                </div>
              </td>
              <td>{{ summary.list_title }}</td>
              <td>{{ summary.list_description }}</td>
              <td>{{ summary.no_cards }}</td>
              <td>{{ summary.no_cards_completed }}</td>
              <td>{{ summary.no_cards_incomplete }}</td>
              <td>{{ summary.no_cards_deadline_crossed_incomplete }}</td>
              <td>{{ summary.no_cards_completed_within_deadline }}</td>
              <td> 
                <div class="btn-group">
                <button class="btn btn-outline-success btn-sm btn-group" v-on:click="goToTrend(summary.id)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-graph-up" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M0 0h1v15h15v1H0V0Zm14.817 3.113a.5.5 0 0 1 .07.704l-4.5 5.5a.5.5 0 0 1-.74.037L7.06 6.767l-3.656 5.027a.5.5 0 0 1-.808-.588l4-5.5a.5.5 0 0 1 .758-.06l2.609 2.61 4.15-5.073a.5.5 0 0 1 .704-.07Z"/>
                  </svg>
                </button>
                <button class="btn btn-outline-success btn-sm btn-group" v-on:click="cardsReport(summary.id)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filetype-csv" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2h-1v-1h1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5ZM3.517 14.841a1.13 1.13 0 0 0 .401.823c.13.108.289.192.478.252.19.061.411.091.665.091.338 0 .624-.053.859-.158.236-.105.416-.252.539-.44.125-.189.187-.408.187-.656 0-.224-.045-.41-.134-.56a1.001 1.001 0 0 0-.375-.357 2.027 2.027 0 0 0-.566-.21l-.621-.144a.97.97 0 0 1-.404-.176.37.37 0 0 1-.144-.299c0-.156.062-.284.185-.384.125-.101.296-.152.512-.152.143 0 .266.023.37.068a.624.624 0 0 1 .246.181.56.56 0 0 1 .12.258h.75a1.092 1.092 0 0 0-.2-.566 1.21 1.21 0 0 0-.5-.41 1.813 1.813 0 0 0-.78-.152c-.293 0-.551.05-.776.15-.225.099-.4.24-.527.421-.127.182-.19.395-.19.639 0 .201.04.376.122.524.082.149.2.27.352.367.152.095.332.167.539.213l.618.144c.207.049.361.113.463.193a.387.387 0 0 1 .152.326.505.505 0 0 1-.085.29.559.559 0 0 1-.255.193c-.111.047-.249.07-.413.07-.117 0-.223-.013-.32-.04a.838.838 0 0 1-.248-.115.578.578 0 0 1-.255-.384h-.765ZM.806 13.693c0-.248.034-.46.102-.633a.868.868 0 0 1 .302-.399.814.814 0 0 1 .475-.137c.15 0 .283.032.398.097a.7.7 0 0 1 .272.26.85.85 0 0 1 .12.381h.765v-.072a1.33 1.33 0 0 0-.466-.964 1.441 1.441 0 0 0-.489-.272 1.838 1.838 0 0 0-.606-.097c-.356 0-.66.074-.911.223-.25.148-.44.359-.572.632-.13.274-.196.6-.196.979v.498c0 .379.064.704.193.976.131.271.322.48.572.626.25.145.554.217.914.217.293 0 .554-.055.785-.164.23-.11.414-.26.55-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.764a.799.799 0 0 1-.118.363.7.7 0 0 1-.272.25.874.874 0 0 1-.401.087.845.845 0 0 1-.478-.132.833.833 0 0 1-.299-.392 1.699 1.699 0 0 1-.102-.627v-.495Zm8.239 2.238h-.953l-1.338-3.999h.917l.896 3.138h.038l.888-3.138h.879l-1.327 4Z"/>
                  </svg>
                </button>
                </div>

              </td>
            </tr>
          </tbody>
    </table>
</div>
  
  <br>
    <div class="container p-5 my-5">
    <FileImportVue />
    </div>

  </div> 


</template>

<script>

import FileImportVue from './FileImport.vue';

export default {

    name: 'SummaryPage',
    data() {
        return{
        user_name: null,
        summary_response:[],
        checked_list:[],
        checked:false,
        file:""

    }},
    components:
    {
      FileImportVue
    },
    methods:{
      goToTrend(id){
        localStorage.setItem("trendline_list_id",id);
        this.$router.push({ path: '/trendline' });
      

      },
      taskListReport(){
        fetch("http://localhost:8000/api/tasklistreport", {
            method: 'GET',
      headers: {
        'Authentication-Token': localStorage.getItem('Authentication-Token')
        }})
        .then(function(response){ if(response.status==200){ alert("Report is being processed. It will be e-mailed shortly!")} else{ return null;}});
      },

      cardsReport(id){
        fetch("http://localhost:8000/api/cardsreport/"+id, {
            method: 'GET',
      headers: {
        'Authentication-Token': localStorage.getItem('Authentication-Token')
        }})
        .then(function(response){ if(response.status==200){ alert("Report is being processed. It will be e-mailed shortly!")} else{ return null;}});

      },

      getAllSelectedCardsReport(){
        if(this.checked_list.length==0){
          alert("No Task List Selected");
        }
        else{

          fetch("http://localhost:8000/api/multiplecardsreport", {
            method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('Authentication-Token')
        },
      body: JSON.stringify({"checked_list": this.checked_list})
      })
      .then(response=>response.json())
        .then(function(response){ alert(response.response)});

        }
               

      },



    },
    mounted(){
        fetch("http://localhost:8000/api/summary", {
            method: 'GET',
      headers: {
        'Authentication-Token': localStorage.getItem('Authentication-Token')
        }})
        .then(function(response){ if(response.status==200){ return response.json();} else{ return null;}})
        .then(response => this.summary_response= response);
        this.user_name=localStorage.getItem("User-Name");
    }




}


</script>