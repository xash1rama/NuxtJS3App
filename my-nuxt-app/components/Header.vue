<template>
  <header>
    <h1 class="header-title">Панель управления Центр СМ</h1>
  </header>
</template>

<script setup>
</script>

<style scoped>
header {
  background-color: #FF5722; /* Цвет фона заголовка, аналогичный цвету футера */
  padding: 1.5rem; /* Увеличен отступ для большей высоты заголовка */
  text-align: center; /* Центрирование текста */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Тень для глубины */
}

.header-title {
  color: white; /* Цвет текста заголовка */
  font-size: 2rem; /* Увеличен размер шрифта заголовка */
  margin: 0; /* Убираем отступы */
  font-weight: bold; /* Жирный шрифт для акцента */
}

/* Подходящее оформление для возможных дополнительных элементов */
.header-title a {
  color: #FFD54F; /* Цвет ссылок, если они добавлены */
  text-decoration: none; /* Убираем подчеркивание */
}

.header-title a:hover {
  text-decoration: underline; /* Подчеркивание при наведении */
}
</style>
