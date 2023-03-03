<template>
 <div class="container-fluid">   
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



<ErrorVue v-if='error' />

<div class="d-flex flex-row flex-wrap py-3" v-else-if='tasklist'>
  <TaskListViewVue v-for='tasks in tasklist'
        
    :key='tasks.id'
    :task='tasks.id'
    :taskName='tasks.list_title'
    :taskDesc='tasks.list_description'
    @taskUpdated="reloadBoard()"
        
  />
</div>

<div v-else-if="!tasklist" style="text-align: center">
  <br>
  <br>
  <button class="btn btn-outline-success btn-lg" v-on:click="newList()">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
      <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
    </svg>
  </button>
  <br>
  <br>
  <FileImportVue />
</div>

<WaitVue v-else />
</div>
</template>

<script>

import TaskListViewVue from './TaskListView.vue';
import ErrorVue from './Error.vue';
import WaitVue from './Wait.vue';
import FileImportVue from './FileImport.vue';

export default{
 name: 'BoardPage',
 data() {
    return {
    tasklist: null,
    user_name: null,
    
    }

 },

 methods: {
  newList: function(){
    this.$router.push({ path: '/newtasklist' });
  },
  async reloadBoard(){
    const response = await fetch("http://localhost:8000/api/task", {
                            method: 'GET',
                            headers: {
                              'Authentication-Token': localStorage.getItem('Authentication-Token')
                              }});
      if(response.status==200)
      {
        const response_json=await response.json();
        this.tasklist=response_json;
      }
      else if(response.status==401)
      {
        this.$router.push({ path: '/logout' });
      }
      else if(response.status==461)
      {
        this.tasklist=null;
      }

  }

 },

 components: {
        TaskListViewVue,
        ErrorVue,
        WaitVue,
        FileImportVue
 },

 async mounted(){

      const response = await fetch("http://localhost:8000/api/task", {
                            method: 'GET',
                            headers: {
                              'Authentication-Token': localStorage.getItem('Authentication-Token')
                              }});
      if(response.status==200)
      {
        const response_json=await response.json();
        this.tasklist=response_json;
      }
      else if(response.status==401)
      {
        this.$router.push({ path: '/logout' });
      }
      

      this.user_name=localStorage.getItem("User-Name");



 }



}
</script>