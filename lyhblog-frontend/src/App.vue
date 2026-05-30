<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script setup>
// 这里什么都不用写了，全部交给路由去管
</script>

<style>
html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  padding: 0;
  min-width: 320px;
  background: #f6f8fb;
  color: #1f2430;
}

body,
button,
input,
textarea {
  font-family:
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
}

button,
input,
textarea {
  font: inherit;
}

#app {
  min-height: 100vh;
}

.front-footer {
  width: min(1168px, calc(100% - 48px));
  margin: 4px auto 0;
  padding: 0 0 42px;
  color: rgba(31, 36, 48, 0.42);
}

.front-footer::before {
  content: "";
  display: block;
  margin: 26px 32px 22px;
  border-top: 1px dashed rgba(31, 36, 48, 0.12);
}

.front-footer-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-align: center;
  font-size: 13px;
  line-height: 1.8;
}

.front-footer-links {
  display: inline-flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.front-footer a {
  color: #2f8df4;
  font-weight: 700;
  text-decoration: none;
  transition: color 0.2s ease, opacity 0.2s ease;
}

.front-footer a:hover {
  color: #257fe3;
  opacity: 0.86;
}

.back-to-top {
  position: fixed;
  right: 28px;
  bottom: 88px;
  z-index: 60;
  width: 54px;
  height: 54px;
  border: 1px solid rgba(31, 36, 48, 0.07);
  border-radius: 16px;
  display: grid;
  place-items: center;
  background: rgba(255, 255, 255, 0.92);
  color: #2f8df4;
  box-shadow:
    0 12px 30px rgba(15, 23, 42, 0.1),
    inset 0 0 0 1px rgba(255, 255, 255, 0.56);
  backdrop-filter: blur(16px);
  cursor: pointer;
  opacity: 0;
  pointer-events: none;
  transform: translateY(12px) scale(0.94);
  transition:
    opacity 0.2s ease,
    transform 0.2s ease,
    background 0.2s ease,
    color 0.2s ease;
}

.back-to-top.is-visible {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0) scale(1);
}

.back-to-top:hover {
  background: #2f8df4;
  color: #fff;
  transform: translateY(-2px) scale(1);
}

.back-to-top:active {
  transform: translateY(0) scale(0.94);
}

.back-to-top-icon {
  font-size: 30px;
  font-weight: 900;
  line-height: 1;
}

@media (max-width: 640px) {
  .front-footer {
    width: min(100% - 28px, 1168px);
    padding-bottom: 30px;
  }

  .front-footer::before {
    margin: 18px 8px 18px;
  }

  .front-footer-inner {
    font-size: 12px;
  }

  .back-to-top {
    right: 14px;
    bottom: 22px;
    width: 48px;
    height: 48px;
    border-radius: 14px;
  }
}
</style>
