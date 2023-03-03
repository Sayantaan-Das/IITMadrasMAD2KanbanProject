<template>
    Logged Out
</template>

<script>
export default{
    name: 'LogOut',
    mounted() {
        localStorage.removeItem('Authentication-Token');
        localStorage.removeItem('User-Name');
        localStorage.removeItem('Task-Id');
        localStorage.removeItem('Task-Description');
        localStorage.removeItem('Task-Title');
        localStorage.removeItem('Card-Id');
        localStorage.removeItem('Card-Title');
        localStorage.removeItem('Card-Content');
        localStorage.removeItem('Card-Deadline');
        localStorage.removeItem('Card-Status');
        localStorage.removeItem('Card-From-List');
        localStorage.removeItem('Card-Status');
        localStorage.removeItem('trendline_list_id');
        this.$router.push({ path: '/' })
    }
}
</script>