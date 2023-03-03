<template>

    <div class="container-fluid">
        <form v-on:submit.prevent="uploadCSV()">
            <label for="file" class="form-label">Upload a CSV File with Task Lists to import it</label>
            <br>
            <br>
            <input type="file" id="file_selector" v-on:change="readFile( $event )">
            <input type="submit" value="Submit">

        </form>
        <br>
        <button class="btn btn-primary-outline btn-sm" v-on:click.prevent="downloadcsvTemplate()">Download csv Template</button>
    </div>


</template>

<script>
export default {

    name: 'ImportFileComponent',

    data() {
        return{

            summary_response:[],
            checked_list:[],
            checked:false,
            file:""

                };
            },

    methods:{

        readFile(e){

            this.file=e.target.files[0]

                    },

        async downloadcsvTemplate()
        {
            const response=await fetch("http://localhost:8000/api/downloadcsvtemplate", 
                            {
                                    method: 'GET',
                            }           );
            if(response.status==200)
            {
                //const response_text=await response.text();
                const response_blob = new Blob([await response.text()], { type: 'text/csv' });
                const url = window.URL.createObjectURL(response_blob)
                const a_tag = document.createElement('a')
                a_tag.setAttribute('href', url)
                a_tag.setAttribute('download', 'CSV_Template.csv');
                a_tag.click()

            }

        },
             


        async uploadCSV(){
            let csv=new FormData();
            csv.set('file',this.file);
            const response_json= await fetch("http://localhost:8000/api/importtasklist", 
                            {
                                    method: 'POST',
                                    headers: {
                                        'Authentication-Token': localStorage.getItem('Authentication-Token')
                                             },
                                    body: csv
                            }           )
                            .then(response=>response.json());
                                
            alert(response_json.response);
                        }

            },
                            }
</script>