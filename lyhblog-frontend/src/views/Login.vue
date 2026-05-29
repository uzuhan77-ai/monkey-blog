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

<style scoped>
div {
  min-height: 100vh;
  padding: 96px 24px 56px;
  position: relative;
  isolation: isolate;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background:
    linear-gradient(120deg, rgba(47, 141, 244, 0.1) 0 1px, transparent 1px 34px),
    linear-gradient(45deg, rgba(28, 188, 155, 0.08) 0 1px, transparent 1px 44px),
    linear-gradient(180deg, #f8fbff 0%, #eef5f9 100%);
  color: #1f2430;
}

div::before {
  content: "";
  position: absolute;
  z-index: -2;
  left: max(24px, 8vw);
  top: 50%;
  width: min(440px, 34vw);
  height: min(540px, 64vh);
  border: 1px solid rgba(255, 255, 255, 0.34);
  border-radius: 28px;
  background:
    linear-gradient(90deg, rgba(255, 255, 255, 0.34), rgba(255, 255, 255, 0.34)) 42px 56px / 92px 7px no-repeat,
    linear-gradient(90deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)) 42px 86px / 210px 6px no-repeat,
    linear-gradient(90deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0.18)) 42px 116px / 155px 6px no-repeat,
    linear-gradient(150deg, rgba(47, 141, 244, 0.92), rgba(28, 188, 155, 0.74));
  box-shadow: 0 28px 80px rgba(34, 80, 130, 0.18);
  transform: translateY(-50%) rotate(-3deg);
}

div::after {
  content: "LYH BLOG  /  Django + Vue";
  position: absolute;
  z-index: -1;
  left: max(52px, 10vw);
  top: calc(50% + 158px);
  padding: 12px 16px;
  border: 1px solid rgba(255, 255, 255, 0.28);
  border-radius: 999px;
  background: rgba(15, 36, 64, 0.18);
  color: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(16px);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

h1,
input,
button {
  position: relative;
  z-index: 1;
  width: min(420px, 100%);
  box-sizing: border-box;
  font: inherit;
}

h1 {
  margin: 0;
  padding: 34px 34px 18px;
  border: 1px solid rgba(31, 36, 48, 0.065);
  border-bottom: 0;
  border-radius: 20px 20px 0 0;
  background: rgba(255, 255, 255, 0.9);
  color: rgba(31, 36, 48, 0.94);
  font-size: 34px;
  line-height: 1.15;
  letter-spacing: 0;
  box-shadow: 0 18px 48px rgba(23, 56, 96, 0.1);
  backdrop-filter: blur(18px);
}

h1::before {
  content: "WELCOME BACK";
  display: block;
  margin-bottom: 10px;
  color: #2f8df4;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

input {
  height: 52px;
  margin: 0;
  padding: 0 18px;
  border: 1px solid rgba(31, 36, 48, 0.065);
  border-bottom-color: rgba(31, 36, 48, 0.035);
  outline: 0;
  background: rgba(255, 255, 255, 0.9);
  color: rgba(31, 36, 48, 0.84);
  font-size: 14px;
  transition: border-color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
}

input:last-of-type {
  border-radius: 0 0 20px 20px;
  box-shadow: 0 20px 48px rgba(23, 56, 96, 0.1);
}

input::placeholder {
  color: rgba(31, 36, 48, 0.36);
}

input:focus {
  z-index: 2;
  border-color: rgba(47, 141, 244, 0.32);
  background: #fff;
  box-shadow: 0 10px 26px rgba(47, 141, 244, 0.12);
}

button {
  min-height: 48px;
  border: 0;
  border-radius: 14px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 800;
  transition: transform 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
}

button:first-of-type {
  margin-top: 22px;
  background: #1f2430;
  color: #fff;
  box-shadow: 0 12px 26px rgba(31, 36, 48, 0.2);
}

button:first-of-type:hover {
  background: #2f8df4;
  box-shadow: 0 14px 30px rgba(47, 141, 244, 0.24);
  transform: translateY(-1px);
}

button:nth-of-type(2) {
  margin-top: 10px;
  border: 1px solid rgba(47, 141, 244, 0.13);
  background: rgba(255, 255, 255, 0.78);
  color: #2f8df4;
  box-shadow: 0 8px 20px rgba(23, 56, 96, 0.06);
}

button:nth-of-type(2):hover {
  background: rgba(47, 141, 244, 0.09);
  transform: translateY(-1px);
}

button:active {
  transform: scale(0.98);
}

@media (min-width: 900px) {
  div {
    align-items: flex-end;
    padding-right: max(8vw, 72px);
  }
}

@media (max-width: 760px) {
  div {
    padding: 84px 18px 36px;
  }

  div::before,
  div::after {
    display: none;
  }

  h1 {
    padding: 30px 26px 16px;
    font-size: 30px;
  }

  input {
    height: 50px;
  }
}
</style>
