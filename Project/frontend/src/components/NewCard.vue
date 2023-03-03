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
      <a class="nav-link active">Kanban Board</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" v-on:click="this.$router.push({ path: '/newtasklist' })">Create New Task List</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" v-on:click="this.$router.push({ path: '/summary' })">Summary</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" v-on:click="this.$router.push({ path: '/profile' })">Profile</a>
    </li>
  </ul>
  
    <div class="container-sm p-5 my-5 bg-dark text-white">
    
        <h1 style="text-align: center;">Add New card in {{ this.card_listName }}</h1>
    
        
        <form v-on:submit="addCard()" style="text-align: center">
    
          <div class="mb-3 mt-3">
              <label for="card_title" class="form-label">Enter Card Title:</label>
              <input type="text" class="form-control" placeholder="Enter Card Title" required="true" v-model="card_title" />
          </div>
    
          <div class="mb-3">    
              <label for="card_content" class="form-label">Enter Content:</label>
              <input type="text" class="form-control" placeholder="Enter Content" required="true" v-model="card_content" />
          </div>
  
          <div class="mb-3">
            <label for="date" class="form-label">Enter Deadline:</label>
            <input class="form-control" type="datetime-local" required="true" v-model="card_deadline"/>
          </div>
  
          <div class="mb-3">
          <label class="radio-inline"><input type="radio" v-model="card_status" value="true">Completed</label>
  <label class="radio-inline"><input type="radio" v-model="card_status" value=null>Not Completed</label>
        </div>
  
        
          <input type="submit" center class="btn btn-primary" />
    
        </form>
    
    </div>


</template>

<script>

export default {
  name: 'NewTaskListPage',

  data() {
    return{
      user_name: null,
      card_title: null,
      card_content: null,
      card_deadline: null,
      card_status: null,
      card_listId: localStorage.getItem('Task-Id'),
      card_listName: localStorage.getItem('Task-Title')
      
    
  };
},
  methods: {
     addCard:    function() {
      
      
      fetch("http://localhost:8000/api/card", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
          },
        body: JSON.stringify({"card_listId":this.card_listId,"card_title": this.card_title, "card_content": this.card_content, "card_deadline":new Date(this.card_deadline).toISOString(),"card_status": this.card_status}), 
      })
      .then( response=>response.json())
      .then(function(response){console.log(response); })
      .catch(error => console.log(error));

      this.$router.push({ path: '/board' });
      

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

      
      
    
      

    },
    async mounted()
    {
      this.user_name=localStorage.getItem("User-Name");
    }
    
  },
}
</script>
