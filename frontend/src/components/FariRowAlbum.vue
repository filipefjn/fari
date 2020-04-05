<template>
    <div ref="albumRowContainer" class="album-container">
        <div class="album-artwork" :style="artworkStyle">
            <!-- <img class="artwork" v-if="displayArtwork" :src="artwork"> -->
        </div>
        <div class="album-info">
            <div class="album-title">{{title}}</div>
            <div class="album-artist"><span v-if="year">{{year}} - </span>{{artist}}</div>
        </div>
    </div>
</template>

<script>

import { mapGetters, mapActions } from "vuex";

export default {
    props: {
        albumId: {
            type: Number,
            required: true,
        },
        artist: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            required: true,
        },
        year: {
            type: String,
        }
    },
    data: function() {
        return {
            displayArtwork: false,
            artwork: ""
        };
    },
    mounted: function() {
        this.$nextTick(function() {
            this.fetchAlbumArtwork();
        });
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
    methods: {
        ...mapActions(['getAlbumArtwork']),
        fetchAlbumArtwork: async function() {
            let artwork = await this.getAlbumArtwork(this.albumId);
            if(artwork) {
                this.artwork = artwork;
                this.displayArtwork = true;
            }
            // OLD
            // if(this.albumId === undefined || this.albumId === null) {
            //     return;
            // }
            // fetch('/api/album-artwork', {
            //     method: 'POST',
            //     headers: {
            //         "Content-Type": "application/json"
            //     },
            //     body: JSON.stringify(
            //         {
            //             "id": this.albumId
            //         }
            //     )
            // }).then((response) => {
            //     if(response.status !== 200) {
            //         console.error("failed to load artwork for " + this.title);
            //         return;
            //     }
            //     return response.json();
            // }).then((response) => {
            //     if(response.artwork) {
            //         this.artwork = response.artwork;
            //         this.displayArtwork = true;
            //     }
            //     console.log("load artwork successful");
            // });
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.album-container {
    display: flex;
    padding: 1rem 0.5rem;
    padding-top: 2rem;
    align-items: center;

    .album-artwork {
        height: 4.5rem;
        width: 4.5rem;
        background-color: #282828;
        overflow: hidden;
        background-repeat: no-repeat;
        background-size: contain;
    }

    .album-info {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        padding-left: 1rem;
        color: $text-color;

        .album-title {
            font-size: 1.25rem;
        }

        .album-artist {
            font-size: 0.9rem;
            margin-top: 0.25rem;
            color: darken($text-color, 20%);
        }
    }
}

</style>
