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
    
        <h1 style="text-align: center;">Move Card {{ card_title }} </h1>
    
        
        <form v-on:submit.prevent="moveCard()" style="text-align: center">
    
          <div class="mb-3 mt-3">
              <label for="card_title" class="form-label">Current Task List:</label>
              <input type="text" class="form-control" placeholder="Enter Card Title" required="true" readonly v-model="current_card_list_title" />
          </div>

          <div class="mb-3 mt-3">
            <label for="update_to_list" class="form-label">Update to Task List:</label>
           


            <select class="form-select" id="update_to_list" required=true v-model="update_to_list_id" >
              <option v-for="valid_list in list_of_valid_list" v-bind:value="valid_list.id" v-bind:key=valid_list.id >{{valid_list.title}}</option>
          </select>

        </div>

  
        
          <input type="submit" center class="btn btn-primary" />
    
        </form>
    
    </div>


</template>

<script>

export default {
  name: 'EditCardPage',

  data() {
    return{
      user_name: null,
      id: null,
      card_title: null,
      current_card_list_title: null,
      list_of_valid_list: null,
      update_to_list_id: null

      
    
  };
},
  methods: {
    async moveCard() {
      
      
      const response = await fetch("http://localhost:8000/api/movecard", {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
          },
        body: JSON.stringify({"card_id":this.id,"update_to_list_id": this.update_to_list_id})});
      
          if (response.status==200)
          {
            alert("Card Moved successfully");
      
          }
          else
          {
            alert("There was some problem in moving the card! Please try again later.")
          }

          this.$router.push({ path: '/board' });
      

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

      
      
    
      

    },
    
  },
  async mounted(){
    this.id= parseInt(localStorage.getItem('Card-Id'));
    this.user_name=localStorage.getItem("User-Name");
    this.card_title= localStorage.getItem('Card-Title');

    const response=await fetch("http://localhost:8000/api/movecard/"+this.id, {
                            method: 'GET',
                            headers: {
                              'Authentication-Token': localStorage.getItem('Authentication-Token')
                              }});

                      if(response.status==200)
                      {
                        const response_json=await response.json();
                        this.current_card_list_title=response_json.current_list_title;
                        this.list_of_valid_list=response_json.list_of_valid_list;
                      }

        
      


      
  }
}
</script>
