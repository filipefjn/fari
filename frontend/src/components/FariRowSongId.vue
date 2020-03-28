<template>
    <FariRowSong
        v-if="song !== null"
        :song="song"
        v-on="listeners"
        v-bind="$attrs"
    />
</template>

<script>
import FariRowSong from '@/components/FariRowSong.vue';

import { mapGetters, mapActions } from 'vuex';

export default {
    props: {
        songId: {
            type: String,
            required: true
        },
    },
    components: {
        FariRowSong
    },
    inheritAttrs: false,
    data: function() {
        return {
            song: null
        }
    },
    watch: {
        songId: {
            handler: function(val) {
                this.updateSong();
            },
            immediate: true
        },
        fullSongList: function() {
            this.updateSong();
        }
    },
    computed: {
        ...mapGetters(['fullSongList']),
        listeners: function() {
            return Object.assign({}, this.$listeners);
        }
    },
    methods: {
        updateSong: function() {
            let found = this.fullSongList.find((item) => {
                if(item.id === this.songId) {
                    return true;
                } else {
                    return false;
                }
            });
            if(found) {
                this.song = found;
            } else {
                this.song = null;
            }
        },
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';


</style>
