<template>
    <div>
        <h1>登录</h1>

        <input type="text" v-model="account" placeholder="账号" />
        <input type="password" v-model="password" placeholder="密码" />

        <button @click="handleLogin">登录</button>
        <button @click="router.push('/register')">没有账号？去注册</button>
        <p style="color: red;">{{ errorMessage }}</p>
    </div>

</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ApiLogin } from '../api/article'
import { useUserStore } from '../stores/user'
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
        if (res.data.code === 200) {
            // 保存 token
            userStore.setToken(res.data.token)

            ElMessage.success('登录成功')

            const redirect = route.query.redirect || '/'
            router.push(redirect)
        }
    }catch(error){
        ElMessage.error('登录失败')
    }
    
}


</script>