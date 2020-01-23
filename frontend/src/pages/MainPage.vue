<template>
    <div class="container">
        <MobileSidebar @change="(content) => selectedContent = content"/>
        <div class="page">
            <Header class="header"/>
            <Sidebar class="sidebar" @change="(content) => selectedContent = content"/>
            <div class="content">
                <transition name="content-transition" v-enter v-leave>
                    <FolderNavigation v-if="selectedContent == 'folders'"/>
                    <Queue            v-if="selectedContent == 'queue'"  />
                </transition>
            </div>
            <MainPageFooter class="footer"/>
        </div>
    </div>

</template>

<script>
import MainPageFooter from '@/components/MainPageFooter.vue';
import Header from '@/components/Header.vue';
import Sidebar from '@/components/Sidebar.vue';
import MobileSidebar from '@/components/MobileSidebar.vue';
import FolderNavigation from '@/components/FolderNavigation.vue';
import Queue from '@/components/Queue.vue';

import { mapGetters } from 'vuex';

export default {
    components: {
        MainPageFooter,
        Header,
        Sidebar,
        MobileSidebar,
        FolderNavigation,
        Queue
    },
    data: function() {
        return {
            selectedContent: '',
        };
    },
    computed: {
        ...mapGetters(['displayMobileSidebar'])
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.container {

    .page {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: $page-bgcolor;
        display: grid;
        grid-template-columns: 12rem auto;
        grid-template-rows: 5rem auto 5rem;

        @include breakpoint(mobile) {
            grid-template-columns: auto;
        }

        .header {
            grid-row: 1 / 2;
            grid-column: 2 / 3;

            @include breakpoint(mobile) {
                grid-column: 1 / 2;
            }

        }

        .sidebar {

            @include breakpoint(not-mobile) {
                grid-row: 1 / 3;
                grid-column: 1 / 2;
            }

            @include breakpoint(mobile) {
                display: none;
            }
        }

        .content {
            grid-row: 2 / 3;
            grid-column: 2 / 3;
            overflow-y: auto;
            position: relative;

            @include breakpoint(mobile) {
                grid-column: 1 / 2;
            }

            &> :last-child {
                padding-bottom: 2rem;
            }
        }

        .footer {
            grid-row: 3 / 4;
            grid-column: 1 / 3;
            background-color: $footer-bgcolor;

            @include breakpoint(mobile) {
                grid-column: 1 / 2;
            }

        }

    }

}



.content-transition-enter-active, .content-transition-leave-active {
    transition: opacity .3s;
    position: absolute;
    top: 0; left: 0; right: 0;
}

.content-transition-enter-active {
    z-index: 300;
}

.content-transition-leave-active {
    z-index: 200;
}

.content-transition-enter, .content-transition-leave-to {
    opacity: 0;
}
</style>
