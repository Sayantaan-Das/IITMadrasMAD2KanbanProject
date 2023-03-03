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

    <div class="container p-5 my-5 bg-dark text-white">
    
        <h1 style="text-align: center;">Edit Task List {{ title }}</h1>
    
        
        <form v-on:submit.prevent="editTaskList()" style="text-align: center">
    
          <div class="mb-3 mt-3">
              <label for="list_title" class="form-label">Task List Title:</label>
              <input type="text" class="form-control" placeholder="Enter Task List Name" required="true" v-model="title" />
          </div>
    
          <div class="mb-3">    
              <label for="list_description" class="form-label">Task List Description:</label>
              <input type="text" class="form-control" placeholder="Enter a Description" required="true" v-model="description" />
          </div>
        
          <input type="submit" center class="btn btn-primary" />
    
        </form>
    
    </div>


</template>

<script>

export default {
  name: 'EditTaskListPage',

  data() {
    return{
        user_name: null,
        id: null,
        title: null,
        description: null,
        
   
  };
},

  methods: {

   async editTaskList() {
      
      try{
      const response= await fetch("http://localhost:8000/api/task/"+this.id, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
          },
        body: JSON.stringify({"list_title": this.title, "list_description": this.description}), 
      });
      if(response.status==200)
      {
        
        localStorage.removeItem('Task-ID');
        localStorage.removeItem('Task-Title');
        localStorage.removeItem('Task-Description');
        this.$router.push({ path: '/board' });
      }

    }catch(e){
        console.log(e);
    }
    
  }},
  mounted(){
    this.id=localStorage.getItem('Task-Id');
        this.title=localStorage.getItem('Task-Title');
        this.description=localStorage.getItem('Task-Description');
        this.user_name=localStorage.getItem("User-Name");
  }
}
</script>
