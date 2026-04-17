<template>
    <el-drawer
      :model-value="modelValue"
      title="AI 写作助手"
      size="520px"
      @close="handleClose"
    >
      <div class="assistant-drawer">
        <el-form :model="queryForm" label-width="88px">
          <el-form-item label="主题">
            <el-input
              v-model="queryForm.topic"
              placeholder="比如：Django + Vue 博客项目部署实战"
            />
          </el-form-item>
  
          <el-form-item label="关键词">
            <el-input
              v-model="queryForm.keywordText"
              placeholder="多个关键词用英文逗号分隔"
            />
          </el-form-item>
  
          <el-form-item label="读者">
            <el-input
              v-model="queryForm.audience"
              placeholder="比如：准备做个人博客项目的初学者"
            />
          </el-form-item>
  
          <el-form-item label="风格">
            <el-select v-model="queryForm.tone" placeholder="选择风格">
              <el-option label="实战型" value="实战型" />
              <el-option label="教程型" value="教程型" />
              <el-option label="总结型" value="总结型" />
            </el-select>
          </el-form-item>
  
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="handleGenerate">
              生成建议
            </el-button>
          </el-form-item>
        </el-form>
  
        <div v-if="result" class="result-panel">
          <div class="panel-header">
            <span>生成结果</span>
            <el-button type="success" plain @click="applyAll">应用全部</el-button>
          </div>
  
          <div class="result-block">
            <div class="result-label">
              标题
              <el-button link type="primary" @click="applyPartial({ title: result.title })">
                应用
              </el-button>
            </div>
            <div class="result-text">{{ result.title }}</div>
          </div>
  
          <div class="result-block">
            <div class="result-label">
              摘要
              <el-button link type="primary" @click="applyPartial({ summary: result.summary })">
                应用
              </el-button>
            </div>
            <div class="result-text">{{ result.summary }}</div>
          </div>
  
          <div class="result-block">
            <div class="result-label">
              分类建议
              <el-button
                link
                type="primary"
                :disabled="!result.category_id"
                @click="applyPartial({ category_id: result.category_id })"
              >
                应用
              </el-button>
            </div>
            <div class="result-text">
              {{ result.category_name || "未匹配到现有分类" }}
            </div>
          </div>
  
          <div class="result-block">
            <div class="result-label">
              标签建议
              <el-button
                link
                type="primary"
                :disabled="!result.matched_tag_ids?.length"
                @click="applyPartial({ matched_tag_ids: result.matched_tag_ids })"
              >
                应用已匹配标签
              </el-button>
            </div>
  
            <div class="tag-list">
              <el-tag
                v-for="tag in result.tag_names"
                :key="tag"
                class="tag-item"
                type="info"
              >
                {{ tag }}
              </el-tag>
            </div>
  
            <div v-if="unmatchedTagNames.length" class="tip-text">
              以下标签未匹配到现有标签，需要你手动新增：{{ unmatchedTagNames.join("、") }}
            </div>
          </div>
  
          <div class="result-block">
            <div class="result-label">提纲建议</div>
            <ol class="outline-list">
              <li v-for="item in result.outline" :key="item">{{ item }}</li>
            </ol>
          </div>
  
          <div class="result-block">
            <div class="result-label">
              Markdown 草稿
              <el-button
                link
                type="primary"
                @click="applyPartial({ content: result.draft_markdown })"
              >
                应用到正文
              </el-button>
            </div>
            <el-input
              :model-value="result.draft_markdown"
              type="textarea"
              :rows="12"
              readonly
            />
          </div>
        </div>
      </div>
    </el-drawer>
  </template>
  
  <script setup>
  import { computed, ref, watch } from "vue";
  import { ElMessage } from "element-plus";
  import { ApiAIWritingAssistant } from "../../api/ai";
  
  const props = defineProps({
    modelValue: {
      type: Boolean,
      default: false,
    },
    articleForm: {
      type: Object,
      required: true,
    },
  });
  
  const emit = defineEmits(["update:modelValue", "apply"]);
  
  const loading = ref(false);
  const result = ref(null);
  const queryForm = ref({
    topic: "",
    keywordText: "",
    audience: "",
    tone: "实战型",
  });
  
  watch(
    () => props.modelValue,
    (visible) => {
      if (visible && !queryForm.value.topic && props.articleForm.title) {
        queryForm.value.topic = props.articleForm.title;
      }
    }
  );
  
  const unmatchedTagNames = computed(() => {
    if (!result.value) return [];
    const matchedSet = new Set(result.value.matched_tag_names || []);
    return (result.value.tag_names || []).filter((item) => !matchedSet.has(item));
  });
  
  function handleClose() {
    emit("update:modelValue", false);
  }
  
  async function handleGenerate() {
    if (!queryForm.value.topic && !props.articleForm.content && !props.articleForm.summary) {
      ElMessage.warning("请先输入主题，或先写一点草稿内容。");
      return;
    }
  
    loading.value = true;
  
    try {
      const payload = {
        topic: queryForm.value.topic,
        keywords: queryForm.value.keywordText
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
        audience: queryForm.value.audience,
        tone: queryForm.value.tone,
        current_title: props.articleForm.title,
        current_summary: props.articleForm.summary,
        current_content: props.articleForm.content,
      };
  
      const res = await ApiAIWritingAssistant(payload);
      if (res.data.code === 200) {
        result.value = res.data.data;
        ElMessage.success("AI 建议已生成");
      } else {
        ElMessage.error(res.data.message || "AI 生成失败");
      }
    } catch (error) {
      ElMessage.error(error.response?.data?.message || "AI 生成失败");
    } finally {
      loading.value = false;
    }
  }
  
  function applyPartial(payload) {
    emit("apply", payload);
  }
  
  function applyAll() {
    if (!result.value) return;
  
    emit("apply", {
      title: result.value.title,
      summary: result.value.summary,
      category_id: result.value.category_id,
      matched_tag_ids: result.value.matched_tag_ids,
      content: result.value.draft_markdown,
    });
  }
  </script>
  
  <style scoped>
  .assistant-drawer {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .result-panel {
    border-top: 1px solid #ebeef5;
    padding-top: 16px;
  }
  
  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    font-weight: 600;
  }
  
  .result-block {
    margin-bottom: 18px;
  }
  
  .result-label {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    font-weight: 600;
  }
  
  .result-text {
    color: #303133;
    line-height: 1.7;
    white-space: pre-wrap;
  }
  
  .tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .tag-item {
    margin-right: 0;
  }
  
  .outline-list {
    padding-left: 18px;
    color: #303133;
    line-height: 1.8;
  }
  
  .tip-text {
    margin-top: 8px;
    color: #909399;
    font-size: 13px;
  }
  </style>