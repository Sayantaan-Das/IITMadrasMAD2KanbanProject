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
        <a class="nav-link active">Create New Task List</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" v-on:click="this.$router.push({ path: '/summary' })">Summary</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" v-on:click="this.$router.push({ path: '/profile' })">Profile</a>
      </li>
    </ul>

    <div class="container p-5 my-5 bg-dark text-white">
    
        <h1 style="text-align: center;">Add New Task List</h1>
    
        
        <form v-on:submit.prevent="addList()" style="text-align: center">
    
          <div class="mb-3 mt-3">
              <label for="list_title" class="form-label">Enter Task List Title:</label>
              <input type="text" class="form-control" placeholder="Enter Task List Name" required="true" v-model="list_title" />
          </div>
    
          <div class="mb-3">    
              <label for="list_description" class="form-label">Enter Description:</label>
              <input type="text" class="form-control" placeholder="Enter a Description" required="true" v-model="list_description" />
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
      last_title: null,
      list_description: null,
      
    
  };
},

  methods: {

     async addList() {
      
      
      const response=await fetch("http://localhost:8000/api/task", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
          },
        body: JSON.stringify({"list_title": this.list_title, "list_description": this.list_description}), 
      });
      if(response.status==200)
      {
      this.$router.push({ path: '/board' })
      }
      

    },
    
  },
  mounted()
  {
    this.user_name=localStorage.getItem("User-Name");
  }
}
</script>
