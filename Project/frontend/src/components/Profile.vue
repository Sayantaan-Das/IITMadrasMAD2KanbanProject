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
          <a class="nav-link" v-on:click="this.$router.push({ path: '/newtasklist' })">Create New Task List</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" v-on:click="this.$router.push({ path: '/summary' })">Summary</a>
        </li>
        <li class="nav-item">
          <a class="nav-link active">Profile</a>
        </li>
      </ul>
      <br>
      <br>
      <div class="container-fluid bg-dark text-white">
        <br>
          <div class="table-responsive">
            <table class="borderless">  
                <tbody>   
                  <tr>
                    <td>Name of the User:</td>
                    <td></td>
                    <td><b>{{ user_name }}</b></td>
                  </tr>
                  <tr>
                    <td>Email ID:</td>
                    <td>  </td>
                    <td><b>{{ email_id }}</b></td>
                  </tr>
                  <tr>
                    <td>Account Created on:</td>
                    <td>  </td>
                    <td><b>{{ created }}</b></td>
                  </tr>
                </tbody>
            </table>
          </div>
        <br>
        <p class="display-2">Preferences:</p>
        <br>
        <label for="format_of_monthly_report">Select the format of your monthly report here (Monthly reports are sent on the 1st of every month for the previous month):</label>
        <select class="form-select" aria-label="format_of_monthly_report" v-model="monthly_report_format">
            <option value="pdf">pdf</option>
            <option value="html">html</option>
        </select>
        <br>
        <div class="form-check form-switch">
          <input class="form-check-input" type="checkbox" id="webhook_reminder_checkbox" v-model="receive_reminders_by_webhook">
          <label class="form-check-label" for="webhook_reminder_checkbox">Receive reminders over Google Workspace via Webhook (Reminders are sent daily at 9:00 PM IST)</label>
        </div>
        <br>
        <label for="webhook_url" class="form-label">Webhook URL to receive daily reminders.</label>
        <input type="text" class="form-control" v-model="webhook_url" placeholder="Enter Webhook URL" />
        <br>
        <button type="button" class="btn btn-danger" v-on:click.prevent="updatePreferences()">Save Preference Changes</button>   
        <br>
        <br>   
      </div>
</template>

<script>
export default
{
    name: 'ProfilePage',
    data()
    {
        return{
            user_name: null,
            email_id: null,
            created: null,
            monthly_report_format: null,
            receive_reminders_by_webhook: null,
            webhook_url: null
                }
    },
    methods:
    {
        async updatePreferences()
        {
            const response=await fetch("http://localhost:8000/api/user",
        {
            method: 'PUT',
            headers:
            {
                'Authentication-Token': localStorage.getItem('Authentication-Token'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                            'monthly_report_format': this.monthly_report_format,
                            'receive_reminders_by_webhook': this.receive_reminders_by_webhook,
                            'webhook_url': this.webhook_url
                                })
        }                           );
                if(response.status==200)
                {
                    const response_json=await response.json();
                    this.user_name=response_json.name;
                    this.email_id=response_json.email;
                    this.created=new Date(response_json.created).getDate();
                    this.monthly_report_format=response_json.monthly_report_format;
                    this.receive_reminders_by_webhook=response_json.receive_reminders_by_webhook;
                    this.webhook_url=response_json.webhook_url;
                    alert("Changes were successfully recorded!");
                }
        }

    },
    async mounted()
    {
        const response=await fetch("http://localhost:8000/api/user",
        {
            method: 'GET',
            headers:
            {
                'Authentication-Token': localStorage.getItem('Authentication-Token')
            }
        }                           );

        if(response.status==200)
        {
            const response_json=await response.json();
            this.user_name=response_json.name;
            this.email_id=response_json.email;
            this.created=new Date(response_json.created).getDate();
            this.monthly_report_format=response_json.monthly_report_format;
            this.receive_reminders_by_webhook=response_json.receive_reminders_by_webhook;
            this.webhook_url=response_json.webhook_url;
        }

    },
}

</script>