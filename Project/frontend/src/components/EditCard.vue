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
      <a class="nav-link active" v-on:click="this.$router.push({ path: '/board' })">Kanban Board</a>
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
    
        <h1 style="text-align: center;">Edit Card " {{ card_title }} "</h1>
    
        
        <form v-on:submit.prevent="editCard()" style="text-align: center">
    
          <div class="mb-3 mt-3">
              <label for="card_title" class="form-label">Card Title:</label>
              <input type="text" class="form-control" placeholder="Enter Card Title" required="true" v-model="card_title" />
          </div>
    
          <div class="mb-3">    
              <label for="card_content" class="form-label">Content:</label>
              <input type="text" class="form-control" placeholder="Enter Content" required="true" v-model="card_content" />
          </div>
  
          <div class="mb-3">
            <label for="date" class="form-label">Deadline:<br> Filled currently as {{card_deadline_display}}. Re-fill this input before submitting! </label>
            <input class="form-control" type="datetime-local" required="true" v-model="card_deadline" />
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
  name: 'EditCardPage',

  data() {
    return{
      user_name: null,
      id: null,
      card_title: null,
      card_content: null,
      card_deadline: null,
      card_status: null,
      card_listId: null,
      card_deadline_display:null
      
    
  };
},
  methods: {
    async editCard() {
      
      
      const response = await fetch("http://localhost:8000/api/card/"+this.id, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('Authentication-Token')
          },
        body: JSON.stringify({"card_listId":this.card_listId,"card_title": this.card_title, "card_content": this.card_content, 'card_deadline':new Date(this.card_deadline), "card_status": this.card_status})});
      
          if (response.status==200)
          {
            alert("Card Updated successfully");
      
          }

          this.$router.push({ path: '/board' });
      

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

      
      
    
      

    },
    
  },
  mounted(){
    this.id= localStorage.getItem('Card-Id');
        this.card_title= localStorage.getItem('Card-Title');
      this.card_content= localStorage.getItem('Card-Content');
      this.card_status= localStorage.getItem('Card-Status');
      
      this.card_listId= localStorage.getItem('Card-From-List');
      this.user_name=localStorage.getItem("User-Name");

      this.card_deadline_display= new Date(localStorage.getItem('Card-Deadline')).toLocaleString();

      if(localStorage.getItem('Card-Status')=="false")
      {
        this.card_status= null; 
      }
  }
}
</script>
