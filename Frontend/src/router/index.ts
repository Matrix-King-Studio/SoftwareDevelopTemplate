import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/Index.vue'
import SignupLogin from '../views/account/SignupLogin.vue'

const routes = [
    {
        path: "/",
        name: "index",
        component: Index
    },
    {
        path: "/signup_login",
        name: "login",
        component: SignupLogin
    }
]

const router = createRouter({
    routes,
    history: createWebHistory()
})

export default router