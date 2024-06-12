<template>
  <div id="app">
    <h1>Smart Shopping List</h1>
    <textarea v-model="textInput" rows="4" cols="50" placeholder="Enter your shopping list here"></textarea><br>
    <button @click="submitText">Generate Current List</button>
    <button @click="fetchShoppingList">Show Complete Shopping List</button>
    <div v-if="response">
      <h2>Generated Shopping List</h2>
      <table>
        <thead>
          <tr>
            <th>Item</th>
            <th>Quantity</th>
            <th>Unit</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in response.items" :key="index">
            <td>{{ item.item }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.unit }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      textInput: '',
      response: null,
    };
  },
  methods: {
    async submitText() {
      if (!this.textInput.trim()) {
        alert('Please enter some text.');
        return;
      }

      try {
        const res = await axios.post('http://127.0.0.1:5000/ab', {
          text: this.textInput
        });
        this.response = res.data;
      } catch (error) {
        console.error('Error generating shopping list:', error);
        alert('Failed to generate shopping list.');
      }
    },
    async fetchShoppingList() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/shopping-list');
        this.response = {
          items: res.data.shopping_list,
        };
      } catch (error) {
        console.error('Error fetching shopping list:', error);
        alert('Failed to fetch shopping list.');
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Arial, Helvetica, sans-serif;
  text-align: center;
  margin-top: 50px;
}
textarea {
  width: 30%;
  margin: 5px auto;
}
button {
  padding: 10px 15px;
  margin: 5px;
  background-color: #13a75d;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 20px;
}
button:hover {
  background-color: #333;
}
table {
  width: 30%;
  margin: 20px auto;
  border-collapse: collapse;
}
th, td {
  padding: 10px;
  border: 1px solid #ddd;
}
th {
  background-color: #f2f2f2;
}
</style>
