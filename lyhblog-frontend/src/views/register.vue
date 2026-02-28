<template>
    <div>
        <h1>注册</h1>
        <input type="text" v-model="account" placeholder="用户名" />
        <input type="password" v-model="password" placeholder="密码" />
        <button @click="handleRegister">注册</button>
        <p style="color: red;">{{ errorMessage }}</p>
        <p style="color: darkblue;">{{ successMessage }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { ApiRegister } from '../api/article'
import router from '../router'
const account = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const handleRegister = async () => {
    if (!account.value || !password.value) {
        errorMessage.value = '用户名和密码不能为空'
        return
    }
    try {
        const res = await ApiRegister({
            account: account.value,
            password: password.value,
        })
        if (res.data.code === 200) {
            successMessage.value = '注册成功'
            setTimeout(() => {
                router.push('/login')
            }, 1500);
        } else {
            errorMessage.value = res.data.message
        }
    }catch(error){
        errorMessage.value = '请求失败'
    }
}
</script>