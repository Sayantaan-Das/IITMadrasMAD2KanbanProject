<template>
  
    <div class="card shadow-sm">
    <div class="card-body p-2">
        <div class="card-title">
            <div class="lead font-weight-light"> <b> {{ card.card_title }} </b> </div>
        

        <div class="btn-group float-end">
        <button class="btn btn-outline-success"  v-on:click="editCard()">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
            </svg>
            </button>
            <button class="btn btn-outline-info" v-on:click="moveCard()">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-card-list" viewBox="0 0 16 16">
                  <path d="M14.5 3a.5.5 0 0 1 .5.5v9a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h13zm-13-1A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 14.5 2h-13z"/>
                  <path d="M5 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 5 8zm0-2.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm0 5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm-1-5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0zM4 8a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0zm0 2.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0z"/>
                </svg>
              </button>

            <button class="btn btn-danger" v-on:click="confirmDeleteCard()">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
              </svg>
          </button>
          
        </div>
      </div>

      <br>

        <p> {{ card_display.card_content }} </p>
        <p> <b>Deadline:</b> {{ card_display.card_deadline }}</p>
       <b> <p v-if='card_display.card_status'>Completed</p>
         <p v-else>Incomplete</p> </b>
        <p> <b>Last Updated on:</b> {{ card_display.card_last_updated }}</p>
        <p> <b>Card Completed On:</b> {{ card_display.card_completed_on }}</p>
        <p> <b>Card Completed within deadline:</b> {{ card_display.card_completed_within_deadline }}</p>

        <button class="btn btn-primary btn-sm" v-on:click="markComplete()" v-if="!card_display.card_status">Mark Complete</button>
    </div>
    </div>
    <br>


      
      

    

</template>

<script>


export default{
    name: "CardView",
    data() {
        return {
            card_display: {},
        };
    },
    props: ["card"],
    
    methods: {
        editCard() {
            this.setID();
            this.$router.push({ path: "/editcard" });
        },
        setID() {
            localStorage.setItem("Card-Id", this.card_display.id);
            localStorage.setItem("Card-Title", this.card_display.card_title);
            localStorage.setItem("Card-Content", this.card_display.card_content);
            localStorage.setItem("Card-Deadline", this.card_display.card_deadline.toISOString());
            localStorage.setItem("Card-Status", this.card_display.card_status);
            localStorage.setItem("Card-From-List", this.card_display.card_listId);
        },
        remID() {
            if (localStorage.getItem("Card-Id")) {
                localStorage.removeItem("Card-Id");
                localStorage.removeItem("Card-Title");
                localStorage.removeItem("Card-Content");
                localStorage.removeItem("Card-Deadline");
                localStorage.removeItem("Card-Status");
                localStorage.removeItem("Card-From-List")
            }
        },

        async moveCard()
        {
            this.setID();
            this.$router.push({ path: "/movecard" });


        },

        async confirmDeleteCard() {

          if(confirm("Are you sure you want to delete the Card? You won't be able to recover it once deleted!"))
          {
            
            const response = await fetch("http://localhost:8000/api/card/" + this.card_display.id, {
                method: "DELETE",
                headers: {
                    "Authentication-Token": localStorage.getItem("Authentication-Token")
                }
            });
            if (response.status == 200) {
                console.log(this.tasklist);
                this.$emit("CardUpdated");
            }
        }},
        async markComplete() {
            const response = await fetch("http://localhost:8000/api/card/" + this.card_display.id, {
                method: "PUT",
                headers: {
                    "Authentication-Token": localStorage.getItem("Authentication-Token"),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "card_listId": this.card_display.card_listId,
                    "card_title": this.card_display.card_title,
                    "card_content": this.card_display.card_content,
                    "card_deadline": this.card_display.card_deadline,
                    "card_status": "true"
                })
            });
            if (response.status == 200) {
                const response_json = await response.json();
                this.card_display = response_json;
                this.card_display.card_deadline = new Date(response_json.card_deadline.concat("Z"));
                this.card_display.card_last_updated = new Date(response_json.card_last_updated);
                if(this.card.card_completed_on)
                {
                this.card_display.card_completed_on=new Date(this.card.card_completed_on);
                }
            }
        },
    },
    async mounted() {
        this.card_display = this.card;

        this.card_display.card_deadline = new Date(this.card.card_deadline.concat("Z"));
        this.card_display.card_last_updated = new Date(this.card.card_last_updated);
        if(this.card_display.card_completed_on)
        {
        
        this.card_display.card_completed_on = new Date(this.card.card_completed_on);
        }
    },

}



</script>