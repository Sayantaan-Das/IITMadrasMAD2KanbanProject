<template>

    <div class="container-fluid">
      <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
        <div class="container-fluid">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" v-on:click="logInPage()">Log In</a>
            </li>
          <li class="nav-item">
              <a class="nav-link active">Create an Account: Enter Details</a>
            </li>
          </ul>
        </div>
      </nav>
    </div>

    <div>
      <center><img src="../assets/logo.png" height="120" width="120" /></center>
    </div>
    <br>

    <div class="container p-5 my-5 bg-dark text-white">
      
      <h1 style="text-align:center">Register a New User Account</h1>
      <br>
      <br>
      <form v-on:submit.prevent="registerUser()" style="text-align: center">
  
        <div class="mb-3 mt-3">
            <label for="emailID" class="form-label">Enter Email ID:</label>
            <input type="email" class="form-control" placeholder="Enter email" required=true v-model="emailID" />
        </div>

        <div class="mb-3">
            <label for="name" class="form-label">Enter Full Name of the User:</label>
            <input type="text" class="form-control" placeholder="Enter Name" required=true v-model="name" />
        </div>
  
        <div class="mb-3">    
            <label for="pwd" class="form-label">Enter Password:</label>
            <input type="password" class="form-control" placeholder="Enter password" required=true v-model="pwd" />
        </div>
      
        <input type="submit" center class="btn btn-primary"/>
  
      </form>
      <br>
      <br>
  
    
  
    </div>
</template>
  
<script>


  export default {
    name: 'RegisterUser',
  
    data() {
      return{
        emailID: "",
        name: "",
        pwd: "",       
      
    };
  },
    
    methods: {

       async registerUser() {

          try{
              const response=await fetch("http://localhost:8000/api/user", {
                  method: 'POST',
                  headers: {
                          'Content-Type': 'application/json',
                          },
                  body:   JSON.stringify({"email": this.emailID, "password": this.pwd, "name":this.name}), 
                  });

              if (response.status==200){
                        const response_json=await response.json();
                        alert("Account created successfully. You can now Log In using your email "+response_json.email);
                        this.$router.push({ path: '/' });
                                        }
              else if(response.status==409){
                        alert("An account with this E-mail ID already exists! Please log in instead of registering again.")
                        this.$router.push({ path: '/' });
                                            }
              else {
                          alert("Account couldn't be created for some internal error. Please try again!")
                    }
              }
              catch(error){ console.log(error);}
                              },

      logInPage(){
          this.$router.push({ path: '/' });
    },
    }
}
</script>
  

  
  