<template>
    <div>
        <np-list>
            <np-list-row header>
                <np-grid-col :span="4">
                    Artist
                </np-grid-col>
                <np-grid-col :span="2" class="text-align-right">
                    Albums
                </np-grid-col>
                <np-grid-col :span="2" class="text-align-right">
                    Songs
                </np-grid-col>
                <np-grid-col :span="2" class="text-align-right">
                    Unrated
                </np-grid-col>
                <np-grid-col :span="2" class="text-align-right">
                    Untagged
                </np-grid-col>
            </np-list-row>
            <np-loading-icon v-if="artists === null" size="120px"></np-loading-icon>
            <np-list-row v-else @click="onArtistClick(artist)" v-for="artist in artists" :key="artist.id">
                <np-grid-col :span="4">
                    {{ artist.name }}
                </np-grid-col>
                <np-grid-col :span="2" class="text-align-right">
                    {{ artist.album_count }}
                </np-grid-col>
                <np-grid-col :span="2" class="text-align-right">
                    {{ artist.song_count }}
                </np-grid-col>
                <np-grid-col :span="2" class="text-align-right">
                    <span v-if="artist.unrated_songs_count">{{ artist.unrated_songs_count }}</span>
                    <span v-else>-</span>
                </np-grid-col>
                <np-grid-col :span="2" class="text-align-right">
                    <span v-if="artist.untagged_songs_count">{{ artist.untagged_songs_count }}</span>
                    <span v-else>-</span>
                </np-grid-col>
            </np-list-row>
        </np-list>
    </div>
</template>

<script>
import NpList from '@/components/NpList.vue';
import NpListRow from '@/components/NpListRow.vue';
import NpListRowButton from '@/components/NpListRowButton.vue';
import NpLoadingIcon from '@/components/NpLoadingIcon.vue';
import NpGridCol from '@/components/NpGridCol.vue';

export default {
    components: {
        NpList,
        NpListRow,
        NpListRowButton,
        NpGridCol,
        NpLoadingIcon
    },
    data: function() {
        return {
            artists: null
        };
    },
    beforeMount: function() {
        this.$store.dispatch('setHeaderInfo', {
            title: "Artists",
            subtitle: ""
        });
    },
    mounted: async function() {
        // fetch artists from server
        let artists = await this.$http.get("/api/v2/artists");
        if(artists.status != 200) {
            console.error(""); // TODO snackbar
        }
        this.artists = artists.data;
    },
    beforeDestroy: function() {
        //
    },
    methods: {
        onArtistClick: function(artist) {
            // TODO open artist
        }
    }
};
</script>
