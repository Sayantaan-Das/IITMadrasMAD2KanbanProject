<template>
<div>
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
</div>
<br>
<br>
<center>
    <div class="col-md-5 px-0 border">

            <img v-bind:src="'data:image/png;base64,'+this.base64_image" class="img-fluid" v-if="base64_image" />
         
</div>
</center>
<div class="container p-5 my-5 bg-dark text-white" v-if="base64_image==0">
  <div class="container-fluid bg-dark text-white">
    <p class="display-2">There is no Trend Line for this Task List</p>
    <br>
   <br>
     <b>Either there are no Cards added or no Cards have been marked as Completed!</b>
     <br>
    <br>
  </div>
</div>
<div class="container p-5 my-5 bg-dark text-white" v-if="base64_image==null">
  <div class="container-fluid bg-dark text-white">
    <p class="display-2">There is no Trend Line for this Task List</p>
    <br>
   <br>
     <b>Either there are no Cards added or no Cards have been marked as Completed!</b>
     <br>
    <br>
  </div>
</div>
</template>

<script>
export default{
    name: 'TrendlinePage',
    data(){
        return{
            user_name: null,
            list_id:localStorage.getItem("trendline_list_id"),
            base64_image:""
        }
    },
    methods:{},
    mounted(){
        fetch("http://localhost:8000/api/trendline/"+this.list_id,
        {
            method: 'GET',
        headers: {
            'Authentication-Token': localStorage.getItem('Authentication-Token')
          },})
      .then( response=>response.json())
      .then(response=> this.base64_image=response.base64_encoded_image)
      .catch(error => console.log(error)); 
      this.user_name=localStorage.getItem("User-Name");
        }


    }

</script>