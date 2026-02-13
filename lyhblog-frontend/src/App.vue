<template>
  <div style="text-align: center; margin-top: 50px;">
    <h1>前端测试页面</h1>
    <div v-if="message" style="margin-bottom: 20px; color: blueviolet;">
      <h3>后端返回结果</h3>
      <p>{{ message }}</p>
    </div>
    <el-element type="primary" @click= "testApi">点击测试后端</el-element>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'
import constant from './utils/constant'
const message = ref('')
const testApi = async() => {
  try {
  const res = await axios.get(constant.baseURL+ '/test/')
  console.log('收到后端数据：', res.data)
  message.value = res.data.message
  }
  catch (error) {
    console.log('请求失败：', error)
    message.value = '请求失败，请检查后端服务'
  }
}
</script>


