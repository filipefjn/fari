<template>
    <div>
        <LoadingPage v-if="loadingScreen"/>
        <MainPage v-else/>
    </div>
</template>

<script>
import MainPage from '@/pages/MainPage.vue';
import LoadingPage from '@/pages/LoadingPage.vue';

import { mapGetters } from 'vuex';

export default {
    name: 'app',
    components: {
        MainPage,
        LoadingPage
    },
    created: function() {
        this.$store.dispatch('createPlayer');
    },
    mounted: function() {
        this.$store.dispatch('fetchFullSongList');
    },
    computed: {
        ...mapGetters(["loadingScreen"])
    }
}
</script>

<style lang="scss">
@import '@/style.scss';

// font import
@import url('https://fonts.googleapis.com/css?family=Monda&display=swap');

// style applied to all html tags
* {
    font-family: 'Monda', sans-serif;
    line-height: 1.5;
    box-sizing: border-box;
}

// change rem unit sizing
html {
    // font-size: 87.5%
}

// remove firefox's button inner border
button::-moz-focus-inner {
    border: 0;
}

// scrollbar css for chrome/chromium
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: #2A2A2A;
}

::-webkit-scrollbar-thumb {
    background: #444444;
}

::-webkit-scrollbar-thumb:hover {
    background: #444444;
}

// scrollbar css for other browsers
* {
    scrollbar-color: #444444 #2A2A2A;
}

body {
    background-color: $page-bgcolor;
}

</style>
