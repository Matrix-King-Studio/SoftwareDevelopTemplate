import {createRouter, createWebHistory} from 'vue-router'

const routes=[
    {
        path:"/",
        name:"index",
        component:()=>import('../views/Index.vue')
    },
    {
        path:"/signup_login",
        name:"login",
        component:()=>import('../views/user/SignupLogin.vue')
    }
]

const router=createRouter({
    routes,
    history:createWebHistory()
})

export default router
