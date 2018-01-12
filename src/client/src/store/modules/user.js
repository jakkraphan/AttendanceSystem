import Cookies from 'js-cookie';

const user = {
    state: {
        user_id: '',
        name: '',
        password: '',
        type: 4,
        information: '',
        department: ''
    },
    mutations: {
        logout (state, vm) {
            Cookies.remove('user');
            localStorage.clear();
        },
        set_user_id (state, id) {
            state.user_id = id;
        },
        set_name (state, name) {
            state.name = name;
        },
        set_password (state, password) {
            state.password = password;
        },
        set_type (state, type) {
            state.type = type;
        },
        set_information (state, information) {
            state.information = information;
        },
        set_department (state, department) {
            state.department = department;
        }
    }
};

export default user;
