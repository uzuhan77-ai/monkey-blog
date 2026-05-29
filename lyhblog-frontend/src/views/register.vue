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
    linear-gradient(120deg, rgba(22, 170, 132, 0.11) 0 1px, transparent 1px 36px),
    linear-gradient(45deg, rgba(47, 141, 244, 0.08) 0 1px, transparent 1px 48px),
    linear-gradient(180deg, #f8fcfb 0%, #eef7fb 100%);
  color: #1f2430;
}

div::before {
  content: "";
  position: absolute;
  z-index: -2;
  right: max(24px, 8vw);
  top: 50%;
  width: min(440px, 34vw);
  height: min(540px, 64vh);
  border: 1px solid rgba(255, 255, 255, 0.34);
  border-radius: 28px;
  background:
    linear-gradient(90deg, rgba(255, 255, 255, 0.34), rgba(255, 255, 255, 0.34)) 42px 56px / 120px 7px no-repeat,
    linear-gradient(90deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)) 42px 88px / 230px 6px no-repeat,
    linear-gradient(90deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0.18)) 42px 120px / 164px 6px no-repeat,
    linear-gradient(150deg, rgba(22, 170, 132, 0.9), rgba(47, 141, 244, 0.72));
  box-shadow: 0 28px 80px rgba(28, 86, 117, 0.17);
  transform: translateY(-50%) rotate(3deg);
}

div::after {
  content: "NEW ACCOUNT  /  Build your notes";
  position: absolute;
  z-index: -1;
  right: max(52px, 10vw);
  top: calc(50% + 158px);
  padding: 12px 16px;
  border: 1px solid rgba(255, 255, 255, 0.28);
  border-radius: 999px;
  background: rgba(9, 52, 53, 0.18);
  color: rgba(255, 255, 255, 0.84);
  backdrop-filter: blur(16px);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

h1 {
  width: min(420px, 100%);
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
  box-sizing: border-box;
  box-shadow: 0 18px 48px rgba(23, 56, 96, 0.1);
  backdrop-filter: blur(18px);
}

h1::before {
  content: "JOIN THE BLOG";
  display: block;
  margin-bottom: 10px;
  color: #16a886;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

input,
button,
p {
  position: relative;
  z-index: 1;
  width: min(420px, 100%);
  box-sizing: border-box;
  font: inherit;
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
  border-color: rgba(22, 168, 134, 0.34);
  background: #fff;
  box-shadow: 0 10px 26px rgba(22, 168, 134, 0.12);
}

button {
  min-height: 48px;
  margin-top: 22px;
  border: 0;
  border-radius: 14px;
  background: #1f2430;
  color: #fff;
  cursor: pointer;
  font-size: 14px;
  font-weight: 800;
  box-shadow: 0 12px 26px rgba(31, 36, 48, 0.2);
  transition: transform 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
}

button:hover {
  background: #16a886;
  box-shadow: 0 14px 30px rgba(22, 168, 134, 0.24);
  transform: translateY(-1px);
}

button:active {
  transform: scale(0.97);
}

p {
  min-height: 20px;
  margin: 10px 0 0 !important;
  padding: 0 2px;
  color: rgba(31, 36, 48, 0.5) !important;
  font-size: 13px;
  line-height: 1.6;
}

p:first-of-type:not(:empty) {
  color: #d95151 !important;
}

p:last-of-type:not(:empty) {
  color: #16a886 !important;
}

@media (min-width: 900px) {
  div {
    align-items: flex-start;
    padding-left: max(8vw, 72px);
  }
}

@media (max-width: 640px) {
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
