<template>
  <aside class="sidebar">
    <div class="card">
      <div class="avatar">LYH</div>
      <h1>LYH BLOG</h1>
      <p>记录AI编程和项目实践</p>
    </div>

    <div class="card">
      <h3>分类</h3>
      <button
      v-for="category in categoryList" 
      :key="category.id"
      :class="{active: categoryId == category.id}"
      @click="$emit('select-category', category.id)"
      >
        {{ category.name }}
      </button>
    </div>


    <div class="card">
      <h3>标签</h3>
      <button 
        v-for="tag in tagList"
        :key="tag.id"
        :class="{active: tagId == tag.id}"
        @click="$emit('select-tag', tag.id)"
      >
        {{ tag.name }}
      </button>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  categoryList: { type: Array, default: () => [] },
  tagList: {type: Array, default: () => []},
  categoryId: {type: [Number, String, null], default: null},
  tagId: {type: [Number, String, null], default: null},
})

defineEmits(['select-category', 'select-tag'])
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-self: start;
  position: sticky;
  top: 94px;
}

.card {
  border: 1px solid rgba(31, 36, 48, 0.06);
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.035);
  backdrop-filter: blur(16px);
}

.card:first-child {
  padding: 14px 14px 20px;
  text-align: center;
}

.avatar {
  width: 100%;
  aspect-ratio: 1 / 0.82;
  margin: 0 auto 16px;
  border-radius: 13px;
  display: grid;
  place-items: center;
  background:
    linear-gradient(135deg, rgba(47, 141, 244, 0.14), rgba(47, 141, 244, 0.045)),
    rgba(47, 141, 244, 0.08);
  color: #2f8df4;
  font-size: 28px;
  font-weight: 800;
  box-shadow: inset 0 0 0 1px rgba(47, 141, 244, 0.08);
}

.card h1,
.card h2 {
  margin: 0;
  color: rgba(31, 36, 48, 0.92);
  font-size: 22px;
  line-height: 1.16;
  letter-spacing: 0;
}

.card p {
  margin: 9px 4px 0;
  color: rgba(31, 36, 48, 0.52);
  font-size: 14px;
  line-height: 1.65;
}

.card:not(:first-child) {
  padding: 18px 18px 14px;
}

.card h3 {
  position: relative;
  margin: 0 0 14px;
  padding-left: 11px;
  color: rgba(31, 36, 48, 0.9);
  font-size: 17px;
  line-height: 1.3;
}

.card h3::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.22em;
  width: 4px;
  height: 1em;
  border-radius: 999px;
  background: #2f8df4;
}

.card button {
  margin: 0 7px 8px 0;
  min-height: 30px;
  padding: 6px 11px;
  border: 0;
  border-radius: 10px;
  background: rgba(47, 141, 244, 0.07);
  color: rgba(47, 111, 171, 0.88);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    background 0.2s ease,
    color 0.2s ease;
}

.card button:hover,
.card button.active {
  background: rgba(47, 141, 244, 0.14);
  color: #2f8df4;
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(47, 141, 244, 0.08);
}

@media (max-width: 900px) {
  .sidebar {
    position: static;
  }

  .card:first-child {
    text-align: left;
  }

  .avatar {
    width: 116px;
    height: 116px;
    aspect-ratio: auto;
    margin-left: 0;
  }
}
</style>
