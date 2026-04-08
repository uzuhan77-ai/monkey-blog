    <template>
        <div>
            <h1>登录</h1>

            <input type="text" v-model="account" placeholder="账号" />
            <input type="password" v-model="password" placeholder="密码" />

            <button @click="handleLogin">登录</button>
            <button @click="router.push('/register')">没有账号？去注册</button>
            <!-- <p style="color: red;">{{ ElMessage }}</p> -->
        </div>

    </template>

    <script setup>
    import { ref } from 'vue'
    import { useRouter, useRoute } from 'vue-router'
    import { ApiLogin } from '../api/article'
    import { useUserStore } from '../stores/user'
    import { ElMessage } from 'element-plus'

    const router = useRouter()
    const route = useRoute()
    const userStore = useUserStore()

    const account = ref('')
    const password = ref('')
    
    const handleLogin =async () => {
        if (!account.value || !password.value) {
            ElMessage.error('账号和密码不能为空')
            return
        }
        try {
            const res = await ApiLogin({
                account: account.value,
                password: password.value,
            })
            console.log(res.data)
            if (res.data.code === 200) {
                //保存 token
                userStore.setLoginInfo(res.data)

                ElMessage.success('登录成功')

                // 跳转之前的页面或者，或首页
                const redirect = route.query.redirect || (res.data.is_admin ? '/admin/article' : '/')
                router.push(redirect)
            }
        }catch(error){
            ElMessage.error(error.response?.data?.message || '登录失败')
        }
        
    }


    </script>