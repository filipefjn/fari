<template>
    <div>
        <div ref="top-ref"></div>
        <np-list>
            <!-- loading -->
            <np-loading-icon v-if="artist_info === null" size="120px"></np-loading-icon>
            <!-- albums -->
            <np-list v-else v-for="album in artist_info.albums" :key="album.id">
                <!-- album info -->
                <np-list-row-album :id="album.id" :title="album.name" :artist="artist_info.name"></np-list-row-album>
                <!-- header -->
                <np-list-row header>
                    <template v-slot:left>
                        <np-list-row-button>
                            <fa-icon icon="play"/>
                        </np-list-row-button>
                    </template>
                    <np-grid-col :span="1" class="text-align-center">#</np-grid-col>
                    <np-grid-col :span="2" class="text-align-center">Duration</np-grid-col>
                    <np-grid-col :span="5">Song</np-grid-col>
                    <np-grid-col :span="4">Artist</np-grid-col>
                    <template v-slot:right>
                        <np-list-row-button>
                            <fa-icon icon="star"/>
                        </np-list-row-button>
                        <np-list-row-button>
                            <fa-icon icon="tags"/>
                        </np-list-row-button>
                        <np-list-row-button>
                            <fa-icon icon="ellipsis-h"/>
                        </np-list-row-button>
                    </template>
                </np-list-row>
                <!-- songs -->
                <np-list-row v-for="song in album.songs" :key="song.id">
                    <template v-slot:left>
                        <np-list-row-button>
                            <fa-icon icon="play"/>
                        </np-list-row-button>
                    </template>
                    <np-grid-col :span="1" class="text-align-center">{{ song.tracknumber }}</np-grid-col>
                    <np-grid-col :span="2" class="text-align-center">{{ song.duration }}</np-grid-col>
                    <np-grid-col :span="5">{{ song.tracktitle }}</np-grid-col>
                    <np-grid-col :span="4">{{ song.artist }}</np-grid-col>
                    <template v-slot:right>
                        <np-list-row-button>
                            <fa-icon icon="star"/>
                        </np-list-row-button>
                        <np-list-row-button>
                            <fa-icon icon="tags"/>
                        </np-list-row-button>
                        <np-list-row-button>
                            <fa-icon icon="ellipsis-h"/>
                        </np-list-row-button>
                    </template>
                </np-list-row>
            </np-list>
        </np-list> 
    </div>
</template>

<script>
import NpList from '@/components/NpList.vue';
import NpListRow from '@/components/NpListRow.vue';
import NpListRowButton from '@/components/NpListRowButton.vue';
import NpListRowAlbum from '@/components/NpListRowAlbum.vue';
import NpLoadingIcon from '@/components/NpLoadingIcon.vue';
import NpGridCol from '@/components/NpGridCol.vue';

export default {
    components: {
        NpList,
        NpListRow,
        NpListRowButton,
        NpListRowAlbum,
        NpGridCol,
        NpLoadingIcon
    },
    data: function() {
        return {
            artist_info: null
        };
    },
    mounted: async function() {
        this.$nextTick(() => {
            this.$refs["top-ref"].scrollIntoView({ block: "start" });
        });
        // fetch artist info from server
        let artist_info = await this.$http.get("/api/v2/artists/" + this.$route.params.slug);
        if(artist_info.status != 200) {
            console.error(""); // TODO snackbar
        }
        this.artist_info = artist_info.data;
        this.$store.dispatch('setHeaderInfo', {
            title: "Artist: " + artist_info.data.name,
            subtitle: ""
        });
    }
}
</script>
