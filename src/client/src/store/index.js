import Vue from 'vue';
import Vuex from 'vuex';

import app from './modules/app';
import user from './modules/user';

Vue.use(Vuex);

const departments = {
    state: {
        departments: {1: '系统管理', 2: '人事管理'}
    },
    mutations: {
        add (state, key, value) {
            state.departments[key] = value;
        },
        remove (state, key) {
            delete state.departments[key];
        },
        set_departments (state, data) {
            const obj = state.departments;
            for (let i of data) {
                obj[i[0]] = i[1];
            }
        }
    }
};

const getters = {
    user_id: state => state.user.user_id,
    name: state => state.user.name,
    password: state => state.user.password,
    type: state => state.user.type,
    information: state => state.user.information,
    department: state => state.user.department,
    departments: state => state.departments.departments
};

const store = new Vuex.Store({
    mutations: {
        //
    },
    actions: {

    },
    modules: {
        app,
        user,
        departments
    },
    getters
});

export default store;
