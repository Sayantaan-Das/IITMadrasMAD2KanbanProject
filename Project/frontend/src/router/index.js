import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Register from '../components/Register.vue';
import Board from '../components/Board.vue'
import Logout from '../components/Logout.vue';
import NewTaskList from '../components/NewTaskList.vue';
import EditTaskList from '../components/EditTaskList.vue';
import NewCard from '../components/NewCard.vue';
import EditCard from '../components/EditCard.vue';
import MoveCard from '../components/MoveCard.vue';
import Summary from '../components/Summary.vue';
import Trendline from '../components/Trendline.vue';
import Profile from '../components/Profile.vue';

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home
    },
    {
        path: "/register",
        name: "Register",
        component: Register
    },
    {
        path: "/board",
        name: "BoardPage",
        component: Board
    },
    {
        path: "/logout",
        name: "LogOut",
        component: Logout
    },
    {
        path: "/newtasklist",
        name: "NewTaskListPage",
        component: NewTaskList
    },
    {
        path: "/edittasklist",
        name: "EditTaskListPage",
        component: EditTaskList
    },
    {
        path: "/newcard",
        name: "NewCardPage",
        component: NewCard
    },
    {
        path: "/editcard",
        name: "EditCardPage",
        component: EditCard
    },
    {
        path: "/movecard",
        name: "MoveCardPage",
        component: MoveCard
    },
    {
        path: "/summary",
        name: "SummaryPage",
        component: Summary
    },
    {
        path: "/trendline",
        name: "TrendlinePage",
        component: Trendline
    },
    {
        path: "/profile",
        name: "ProfilePage",
        component: Profile
    },
]

const router=createRouter({
    history: createWebHistory(),
    routes,});

export default router;