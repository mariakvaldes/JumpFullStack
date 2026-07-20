import apiClient from './apiClient';

export const bankService = {
  // Auth & Customers
  login: async (formData) => {
    // OAuth2PasswordRequestForm expects form-data
    const response = await apiClient.post('/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    return response.data;
  },
  registerCustomer: async (customerData) => {
    const response = await apiClient.post('/customers', customerData);
    return response.data;
  },

  // Accounts
  getAllAccounts: async () => {
    const response = await apiClient.get('/accounts');
    return response.data;
  },
  createAccount: async (accountData) => {
    const response = await apiClient.post('/accounts', accountData);
    return response.data;
  },
  getAccountById: async (id) => {
    const response = await apiClient.get(`/accounts/${id}`);
    return response.data;
  },
  getBalance: async (id) => {
    const response = await apiClient.get(`/accounts/${id}/balance`);
    return response.data;
  },
  deleteAccount: async (id) => {
    const response = await apiClient.delete(`/accounts/${id}`);
    return response.data;
  },

  // Transactions & Operations
  depositMoney: async (id, amount) => {
    const response = await apiClient.post(`/accounts/${id}/deposit`, { amount });
    return response.data;
  },
  withdrawMoney: async (id, amount) => {
    const response = await apiClient.post(`/accounts/${id}/withdraw`, { amount });
    return response.data;
  },
  getTransactions: async (id, type = '', sort = 'desc') => {
    const query = type ? `?type=${type}&sort=${sort}` : `?sort=${sort}`;
    const response = await apiClient.get(`/accounts/${id}/transactions${query}`);
    return response.data;
  }
};