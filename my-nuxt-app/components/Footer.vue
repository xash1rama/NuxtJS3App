<template>
  <footer>
    <div class="footer-container">
      <p class="footer-text">&copy; 2025 Вологда</p>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
footer {
  background-color: #FF5722; /* Основной цвет, совпадающий с остальной частью интерфейса */
  padding: 1rem;
  text-align: center;
  color: white; /* Цвет текста для лучшего контраста */
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1); /* Небольшая тень для создания глубины */
}

.footer-container {
  max-width: 1200px; /* Ограничение ширины контейнера для аккуратного отображения */
  margin: 0 auto; /* Центрирование содержимого */
}

.footer-text {
  margin: 0; /* Убираем отступы */
  font-size: 1rem; /* Размер шрифта */
}

/* Стиль для нихи, если нужно добавить дополнительные элементы */
.footer-text a {
  color: #FFD54F; /* Цвет ссылок */
  text-decoration: none; /* Убираем подчеркивание */
}

.footer-text a:hover {
  text-decoration: underline; /* Подчеркивание ссылки при наведении */
}
</style>

