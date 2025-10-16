import { api } from './api';

export const postsService = {
  async getAllPosts() {
    try {
      const response = await api.get('/api/posts/');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  async createPost(postData) {
    try {
      const response = await api.post('/api/posts/', postData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  async getPostById(id) {
    try {
      const response = await api.get(`/api/posts/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  async updatePost(id, postData) {
    try {
      const response = await api.put(`/api/posts/${id}`, postData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  async deletePost(id) {
    try {
      const response = await api.delete(`/api/posts/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  }
};
