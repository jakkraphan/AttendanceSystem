import Main from '@/views/Main.vue';

// 不作为Main组件的子页面展示的页面单独写，如下
export const loginRouter = {
    path: '/login',
    name: 'login',
    meta: {
        title: 'Login - 登录'
    },
    component: resolve => { require(['@/views/login.vue'], resolve); }
};

export const page404 = {
    path: '/*',
    name: 'error-404',
    meta: {
        title: '404-页面不存在'
    },
    component: resolve => { require(['@/views/error-page/404.vue'], resolve); }
};

export const page403 = {
    path: '/403',
    meta: {
        title: '403-权限不足'
    },
    name: 'error-403',
    component: resolve => { require(['@//views/error-page/403.vue'], resolve); }
};

export const page500 = {
    path: '/500',
    meta: {
        title: '500-服务端错误'
    },
    name: 'error-500',
    component: resolve => { require(['@/views/error-page/500.vue'], resolve); }
};

// 作为Main组件的子页面展示但是不在左侧菜单显示的路由写在otherRouter里
export const otherRouter = {
    path: '/',
    name: 'otherRouter',
    component: Main,
    children: [
        { path: 'home', title: {i18n: 'home'}, name: 'home_index', component: resolve => { require(['@/views/home/home.vue'], resolve); } }
    ]
};

// 作为Main组件的子页面展示并且在左侧菜单显示的路由写在appRouter里
export const appRouter = [
    {
        path: '/page',
        icon: 'android-settings',
        title: 'Setting',
        name: 'setting',
        component: Main,
        children: [
            {
                path: 'setting',
                title: 'Setting',
                name: 'page_setting',
                component: resolve => { require(['@/views/page/setting.vue'], resolve); }
            }
        ]
    },
    {
        path: '/page',
        icon: 'calendar',
        title: 'Attendance',
        name: 'attendance',
        component: Main,
        children: [
            {
                path: 'attendance',
                title: 'Attendance',
                name: 'page_attendance',
                component: resolve => { require(['@/views/page/attendance.vue'], resolve); }
            }
        ]
    },
    {
        path: '/page',
        icon: 'navigate',
        title: 'Leave',
        name: 'leave',
        component: Main,
        children: [
            {
                path: 'leave',
                title: 'Leave',
                name: 'page_leave',
                component: resolve => { require(['@/views/page/leave.vue'], resolve); }
            }
        ]
    },
    {
        path: '/page',
        icon: 'plane',
        title: 'Business trip',
        name: 'trip',
        component: Main,
        children: [
            {
                path: 'trip',
                title: 'Business trip',
                name: 'page_trip',
                component: resolve => { require(['@/views/page/trip.vue'], resolve); }
            }
        ]
    },
    {
        path: '/page',
        icon: 'person-stalker',
        title: 'Employee',
        name: 'employee',
        component: Main,
        children: [
            {
                path: 'employee',
                title: 'Employee',
                name: 'page_employee',
                component: resolve => { require(['@/views/page/employee.vue'], resolve); }
            }
        ]
    },
    {
        path: '/page',
        icon: 'ios-book',
        title: 'Log',
        name: 'log',
        component: Main,
        children: [
            {
                path: 'log',
                title: 'Log',
                name: 'page_log',
                component: resolve => { require(['@/views/page/log.vue'], resolve); }
            }
        ]
    }
];

// 所有上面定义的路由都要写在下面的routers里
export const routers = [
    loginRouter,
    otherRouter,
    ...appRouter,
    page500,
    page403,
    page404
];
