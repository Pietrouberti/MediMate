import { defineStore } from 'pinia';
import axios from 'axios';

// pinia store to hold user information within browser for quick frontend autehntication and data handling

export const useUserStore = defineStore('user', {
    id: 'user',
    state: () => ({
        user: {
            id : '',
            name: '',
            email: '',
            accessToken: '',
            refreshToken: '',
            isAuthenticated: false,
        }
    }),
    actions: {  
        initStore() {
            if (localStorage.getItem('user.accessToken')) {
                this.user.accessToken = localStorage.getItem('user.accessToken');
                this.user.refreshToken = localStorage.getItem('user.refreshToken');
                this.user.id = localStorage.getItem('user.id');
                this.user.name = localStorage.getItem('user.name');
                this.user.email = localStorage.getItem('user.email');
                this.user.isAuthenticated = true;

                this.refreshTokenFunc();

                console.log('Initalised User: ', this.user);
            }
        },
        refreshTokenFunc() {
            axios.post('/api/doctor/refresh/', {
                refresh: this.user.refreshToken
            }).then((response) => {
                this.user.accessToken = response.data.access;
                localStorage.setItem('user.accessToken', response.data.access);
                axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
            }).catch((error) => {
                console.error('Error refreshing token: ', error);
                this.removeToken();
            })
        },
        removeToken() {
            this.user.accessToken = '';
            this.user.refreshToken = '';
            this.user.isAuthenticated = false;
            this.user.id = '';
            this.user.name = '';
            this.user.email = '';
            
            localStorage.removeItem('user.accessToken');
            localStorage.removeItem('user.refreshToken');
            localStorage.removeItem('user.id');
            localStorage.removeItem('user.name');
            localStorage.removeItem('user.email');
            localStorage.removeItem('user.isAuthenticated');
        },
        setToken(data) {
            this.user.accessToken = data.access;
            this.user.refreshToken = data.refresh;
            this.user.isAuthenticated = true;
            localStorage.setItem('user.accessToken', data.access);
            localStorage.setItem('user.refreshToken', data.refresh);

            console.log('Set Token: ', this.user);
        },
        setUserInfo(user) {
            const userData = user.user;
        
            this.user.id = userData.id;
            this.user.name = userData.name;
            this.user.email = userData.email;
            
            localStorage.setItem('user.id', userData.id);
            localStorage.setItem('user.name', userData.name);
            localStorage.setItem('user.email', userData.email);
        },

    }
});