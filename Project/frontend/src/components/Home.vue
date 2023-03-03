<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
      <div class="container-fluid">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link active">Log In</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" v-on:click="registerUser()">Create an Account</a>
          </li>
        </ul>
      </div>
    </nav>
  </div>

  <div>
    <center><img src="../assets/logo.png" height="120" width="120" /></center>
  </div>

  <div class="container p-5 my-5 bg-dark text-white">
    
    <h1>Welcome to the Kanban App by Sayantan Das</h1>
    
    <form v-on:submit.prevent="loginfunction()" style="text-align: center">

      <div class="mb-3 mt-3">
          <label for="emailID" class="form-label">Enter Email ID:</label>
          <input type="email" class="form-control" placeholder="Enter email" v-model="emailID" />
          <div class="invalid-feedback">
            Please enter an E-mail id:
          </div>
      </div>

      <div class="mb-3">    
          <label for="pwd" class="form-label">Enter Password:</label>
          <input type="password" class="form-control" placeholder="Enter password" v-model="pwd" />
      </div>
    
      <input type="submit" center class="btn btn-primary"/>

    </form>

  </div>
</template>

<script>

export default {
  name: 'HomePage',

  data() {
    return{
      emailID: "",
      pwd: "",
    
  };
},
  methods: {
   async loginfunction() {
      
      
    const response= await fetch("http://localhost:8000/login?include_auth_token", {
                          method: 'POST',
                          headers: {
                            'Content-Type': 'application/json',
                            },
                          body: JSON.stringify({"email": this.emailID, "password": this.pwd})       });

                
      
                if(response.status==200) {  
                    const response_json=await response.json();
                    console.log(response_json);
                    localStorage.setItem("Authentication-Token",response_json.response.user.authentication_token);
                    localStorage.setItem("User-Name",response_json.response.user.name);
                    this.$router.push({ path: '/board' });}
                else {
                  alert("Either the ID or the password is incorrect! Or an account for the same does not exist.\nConsider creating an account!");

                      }
                    },   
        


    registerUser(){
      this.$router.push({ path: '/register' }); 
    },
    
  },
}
</script>



