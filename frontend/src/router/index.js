import Vue from 'vue';
import VueRouter from 'vue-router';
import MainLayout from '../layouts/MainLayout.vue';
import HomeView from '../views/HomeView.vue';
import ArtistsView from '../views/ArtistsView.vue';
import NotFoundView from '../views/NotFoundView.vue';

Vue.use(VueRouter);

// TODO code splitting

const routes = [
    {
        path: '/',
        name: 'Home',
        components: {
            layout: MainLayout,
            view: HomeView
        }
    },
    {
        path: '/artists',
        name: 'Artists',
        components: {
            layout: MainLayout,
            view: ArtistsView
        }
    },
    {
        path: '*',
        components: {
            layout: MainLayout,
            view: NotFoundView
        }
    }
    //   {
    //     path: '/about',
    //     name: 'About',
    //     // route level code-splitting
    //     // this generates a separate chunk (about.[hash].js) for this route
    //     // which is lazy-loaded when the route is visited.
    //     component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    //   }
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
});

export default router;
