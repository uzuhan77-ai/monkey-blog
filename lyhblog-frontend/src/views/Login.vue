<template>
    <div>
        <h1>登录</h1>

        <input type="text" v-model="account" placeholder="账号" />
        <input type="password" v-model="password" placeholder="密码" />

        <button @click="handleLogin">登录</button>
        <p style="color: red;">{{ errorMessage }}</p>
    </div>

</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ApiLogin } from '../api/article'
const router = useRouter()
const route = useRoute()
const account = ref('')
const password = ref('')
const errorMessage = ref('')
const handleLogin =async () => {
    if (!account.value || !password.value) {
        errorMessage.value = '账号和密码不能为空'
        return
    }
    try {
        const res = await ApiLogin({
            account: account.value,
            password: password.value,
            province: ''
        })
        console.log(res.data)
        if (res.data.code === 200) {
            errorMessage.value = "登录成功"
            localStorage.setItem('user_token',res.data.token)
            const redirect = route.query.redirect || '/'
            router.push(redirect)
        } else {
        errorMessage.value = res.data.message
        }
    }catch(error){
        errorMessage.value = "服务器错误"
    }
    
}


</script>