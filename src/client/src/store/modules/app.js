import {otherRouter, appRouter} from '@/router/router';
import Cookies from 'js-cookie';

const app = {
    state: {
        menuList: [],
        routers: [
            otherRouter,
            ...appRouter
        ]
    },
    mutations: {
        updateMenulist (state) {
            const mode = Cookies.get('mode');
            const mAccess = mode !== undefined ? parseInt(mode) : 0;
            let menuList = [];
            appRouter.forEach(item => {
                if (item.access === undefined || mAccess >= item.access) {
                    menuList.push(item);
                }
            });
            state.menuList = menuList;
        }
    }
};

export default app;
