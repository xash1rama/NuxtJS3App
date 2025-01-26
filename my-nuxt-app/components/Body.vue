<template>
  <div>
    <h1>Пользователи</h1>
    <!-- Форма создания пользователя -->
    <form @submit.prevent="createUser ">
      <div class="form-group">
        <input v-model="newUser .name" placeholder="Имя" required />
        <input v-model="newUser .last_name" placeholder="Фамилия" required />
        <input v-model="newUser .email" placeholder="Email (валидация именно на email)" required />
        <input v-model="newUser .phone" placeholder="Телефон (валидация +71234567890)" required />
        <button type="submit" class="btn">Создать пользователя</button>
      </div>
    </form>

    <!-- Таблица пользователей -->
    <table class="user-table">
      <thead>
        <tr>
          <th>Имя</th>
          <th>Фамилия</th>
          <th>Email</th>
          <th>Телефон</th>
          <th>Роль</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.email">
          <td>{{ user.name }}</td>
          <td>{{ user.last_name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.phone }}</td>
          <td>{{ user.role }}</td>
          <td>
            <button @click="deleteUser (user.id)" class="action-btn">Удалить</button>
            <button @click="startEditingUser (user)" class="action-btn">Редактировать</button>
            <button @click="startEditingRole(user)" class="action-btn">Обновить роль</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Форма редактирования пользователя -->
    <div v-if="isEditing">
      <h2>Редактировать пользователя</h2>
      <form @submit.prevent="updateUser (editingUser .id)">
        <div class="form-group">
          <input v-model="editingUser .name" placeholder="Имя" required />
          <input v-model="editingUser .last_name" placeholder="Фамилия" required />
          <input v-model="editingUser .email" placeholder="Email (валидация именно на email)" required />
          <input v-model="editingUser .phone" placeholder="Телефон (валидация +71234567890)" required />
          <button type="submit" class="btn">Редактировать</button>
          <button type="button" @click="cancelEdit" class="btn">Отмена</button>
        </div>
      </form>
    </div>

    <!-- Форма редактирования роли -->
    <div v-if="isEditingRole">
      <h2>Обновить роль</h2>
      <form @submit.prevent="updateRole(editingRole.id)" autocomplete="off">
        <div class="form-group">
          <input v-model="editingRole.name" placeholder="Название роли" required autocomplete="off" />
          <input v-model="editingRole.description" placeholder="Описание роли" required autocomplete="off" />
          <button type="submit" class="btn">Обновить</button>
          <button type="button" @click="cancelEditRole" class="btn">Отмена</button>
        </div>
      </form>
    </div>

    <!-- Новая таблица для отображения ролей -->
    <h1>Роли пользователей</h1>
    <table class="role-table">
      <thead>
        <tr>
          <th>Название роли</th>
          <th>Описание</th>
          <th>Пользователь</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="role in roles" :key="role.id">
          <td>{{ role.role }}</td>
          <td>{{ role.description }}</td>
          <td>{{ role.user }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const users = ref([]);
    const roles = ref([]);
    const newUser  = ref({ name: '', last_name: '', email: '', phone: '' });
    const editingUser  = ref({ id: null, name: '', last_name: '', email: '', phone: '' });
    const editingRole = ref({ id: null, role: '', description: '' });
    const isEditing = ref(false);
    const isEditingRole = ref(false);

    const fetchUsers = async () => {
      try {
        const response = await fetch('http://localhost:8000/user/');
        const data = await response.json();
        users.value = data.users;
      } catch (error) {
        const editingRole = ref({ id: null, name: '', description: '' });
      }
    };

    const fetchRoles = async () => {
      try {
        const response = await fetch('http://localhost:8000/user/roles');
        const data = await response.json();
                roles.value = data.roles;
      } catch (error) {
        console.error('Ошибка при получении ролей:', error);
      }
    };

    const createUser  = async () => {
      try {
        await fetch('http://localhost:8000/user/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newUser .value),
        });
        await fetchUsers(); // Обновляем список после редактирования
        await fetchRoles(); // Обновляем список ролей после редактирования
        newUser .value = { name: '', last_name: '', email: '', phone: '' }; // Сбрасываем форму
      } catch (error) {
        console.error('Ошибка при создании пользователя:', error);
      }
    };

    const deleteUser  = async (id) => {
      try {
        await fetch(`http://localhost:8000/user/${id}`, {
          method: 'DELETE',
        });
        await fetchUsers(); // Обновляем список после редактирования
        await fetchRoles(); // Обновляем список ролей после редактирования
      } catch (error) {
        console.error('Ошибка при удалении пользователя:', error);
      }
    };

    const startEditingUser  = (user) => {
      editingUser .value = { ...user }; // Копируем данные редактируемого пользователя
      isEditing.value = true;
    };

    const updateUser  = async (id) => {
      try {
        await fetch(`http://localhost:8000/user/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(editingUser .value),
        });
        await fetchUsers(); // Обновляем список после редактирования
        await fetchRoles(); // Обновляем список ролей после редактирования
        cancelEdit(); // Сбрасываем форму редактирования
      } catch (error) {
        console.error('Ошибка при обновлении пользователя:', error);
      }
    };

    const cancelEdit = () => {
      isEditing.value = false;
      editingUser .value = { id: null, name: '', last_name: '', email: '', phone: '' }; // Сброс формы
    };

    const startEditingRole = (role) => {
  editingRole.value = { id: role.id, name: role.role, description: role.description }; // Копируем данные редактируемой роли
  isEditingRole.value = true;
};


    const updateRole = async (id) => {
  try {
    await fetch(`http://localhost:8000/user/roles/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: editingRole.value.name,
        description: editingRole.value.description,
      }),
    });
    await fetchRoles(); // Обновляем список ролей после редактирования
    await fetchUsers(); // Обновляем список после редактирования
    cancelEditRole(); // Сбрасываем форму редактирования роли
  } catch (error) {
    console.error('Ошибка при обновлении роли:', error);
    console.log(`Обновление роли: `, editingRole.value);
  }
};


    const cancelEditRole = () => {
      isEditingRole.value = false;
      editingRole.value = { id: null, role: '', description: '' }; // Сброс формы
    };

    // Инициализация данных при загрузке компонента
    onMounted(() => {
      fetchUsers();
      fetchRoles();
    });

    return {
      users,
      roles,
      newUser ,
      editingUser ,
      editingRole,
      isEditing,
      isEditingRole,
      createUser ,
      deleteUser ,
      startEditingUser ,
      updateUser ,
      cancelEdit,
      startEditingRole,
      updateRole,
      cancelEditRole,
    };
  },
};
</script>

<style scoped>
/* Стили для форм */
.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

input {
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn {
  padding: 10px;
  background-color: #FF5722; /* Цвет кнопок */
    color: white; /* Цвет текста кнопок */
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #e64a19; /* Цвет кнопок при наведении */
}

/* Стили для таблицы пользователей */
.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.user-table th, .user-table td {
  padding: 12px;
  border: 1px solid #ccc;
  text-align: left;
}

.user-table th {
  background-color: #f5f5f5; /* Цвет фона заголовков */
}

.user-table tr:nth-child(even) {
  background-color: #f9f9f9; /* Цвет четных строк */
}

/* Стили для таблицы ролей */
.role-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.role-table th, .role-table td {
  padding: 12px;
  border: 1px solid #ccc;
  text-align: left;
}

.role-table th {
  background-color: #e0e0e0;
}

.role-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

/* Стили для кнопок действий в таблицах */
.action-btn {
  padding: 8px 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.action-btn:hover {
  background-color: #1976D2;
}
</style>





