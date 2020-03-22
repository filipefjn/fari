<template>
    <div class="container">
        <FariSidebarMobile @change="(content) => selectedContent = content"/>
        <div class="page">
            <FariHeader class="header">
                <template v-slot:right>
                    <FariHeaderButton :selected="!!listParams.isNarrow" @click="toggleNarrow()">
                        <fa-icon icon="compress-arrows-alt"/>
                    </FariHeaderButton>
                    <FariHeaderButton :selected="!!listParams.showTags" @click="toggleTags()">
                        <fa-icon icon="tags"/>
                    </FariHeaderButton>
                </template>
            </FariHeader>
            <FariSidebar class="sidebar" @change="(content) => selectedContent = content"/>
            <div class="content">
                <transition name="content-transition" v-enter v-leave>
                    <keep-alive exclude="FariViewSongs">
                        <component :is="contentComponent"></component>
                    </keep-alive>
                </transition>
            </div>
            <FariFooterMobile class="mobile-footer"/>
            <FariFooter class="footer"/>
        </div>
    </div>

</template>

<script>
import FariFooter from '@/components/FariFooter.vue';
import FariFooterMobile from '@/components/FariFooterMobile.vue';
import FariHeader from '@/components/FariHeader.vue';
import FariSidebar from '@/components/FariSidebar.vue';
import FariSidebarMobile from '@/components/FariSidebarMobile.vue';
import FariViewFolders from '@/components/FariViewFolders.vue';
import FariViewQueue from '@/components/FariViewQueue.vue';
import FariViewSongs from '@/components/FariViewSongs.vue';
import FariViewArtists from '@/components/FariViewArtists.vue';
import FariViewFilterTags from '@/components/FariViewFilterTags.vue';
import FariHeaderButton from '@/components/FariHeaderButton.vue';

import { mapGetters } from 'vuex';

export default {
    components: {
        FariFooter,
        FariFooterMobile,
        FariHeader,
        FariSidebar,
        FariSidebarMobile,
        FariViewFolders,
        FariViewQueue,
        FariViewSongs,
        FariViewArtists,
        FariViewFilterTags,
        FariHeaderButton
    },
    data: function() {
        return {
            selectedContent: '',
        };
    },
    computed: {
        ...mapGetters(['displayMobileSidebar', 'listParams']),
        contentComponent: function () {
            switch(this.selectedContent) {
                case "folders":
                    return "FariViewFolders";
                    break;
                case "queue":
                    return "FariViewQueue";
                    break;
                case "allsongs":
                    return "FariViewSongs";
                    break;
                case "artists":
                    return "FariViewArtists";
                    break;
                case "filtertags":
                    return "FariViewFilterTags";
                    break;
                default:
                    return null;
                    break;
            }
        }
    },
    methods: {
        toggleTags: function() {
            this.$store.dispatch('setListParams', {showTags: !this.listParams.showTags});
        },
        toggleNarrow: function() {
            this.$store.dispatch('setListParams', {isNarrow: !this.listParams.isNarrow});
        }
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
            grid-template-rows: 5rem auto 4rem;
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
                display: none;
            }

        }

        .mobile-footer {
            grid-row: 3 / 4;
            grid-column: 1 / 2;
            background-color: $footer-bgcolor;
            display: none;

            @include breakpoint(mobile) {
                display: initial;
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
