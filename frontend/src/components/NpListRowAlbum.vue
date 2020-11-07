<template>
    <div class="np-list-row-album">
        <div class="np-list-row-album-art" :style="artworkStyle">
            <np-loading-icon v-if="loading" size="3.5rem"></np-loading-icon>
        </div>
        <div class="np-list-row-album-info">
            <div class="np-list-row-album-info-title">{{ title }}</div>
            <div>{{ artist }}</div>
        </div>
    </div>
</template>

<script>
import NpLoadingIcon from '@/components/NpLoadingIcon.vue';

import { mapGetters, mapActions } from "vuex";

export default {
    props: {
        id: {
            type: Number,
            required: true
        },
        title: {
            type: String,
            required: true
        },
        artist: {
            type: String,
            required: true
        }
    },
    components: {
        NpLoadingIcon
    },
    data: function() {
        return {
            loading: true,
            displayArtwork: true,
            artwork: null
        };
    },
    computed: {
        artworkStyle: function() {
            let style = {};
            if(this.displayArtwork) {
                style["background-image"] = 'url("' + this.artwork + '")';
            }
            return style;
        }
    },
    mounted: function() {
        this.fetchArtwork();
    },
    methods: {
        ...mapActions(['getAlbumArtwork']),
        fetchArtwork: async function() {
            let artwork = await this.getAlbumArtwork(this.id);
            if(artwork) {
                this.artwork = artwork;
                this.displayArtwork = true;
                this.loading = false;
            }
        }
    }
}
</script>