<template>
    <div class="container">
        <FariList>
            <FariRowSimple v-if="currentDir !== '/'" @click="openSubfolder('..')">
                <FariRowIcon><fa-icon icon="level-up-alt"/></FariRowIcon>
                ..
            </FariRowSimple>
            <FariRowSimple v-for="item in subfolders" @click="openSubfolder(item)" :key="item">
                <FariRowIcon><fa-icon icon="folder"/></FariRowIcon>
                {{item}}
            </FariRowSimple>
            <FariRowSimple v-for="item in files" :key="item" @click="queueFolder(item)">
                <FariRowIcon><fa-icon icon="music"/></FariRowIcon>
                {{item}}
            </FariRowSimple>
        </FariList>
    </div>
</template>

<script>
import FariList from '@/components/FariList.vue';
import FariRowSimple from '@/components/FariRowSimple.vue';
import FariRowIcon from '@/components/FariRowIcon.vue';
import { mapActions } from 'vuex';

export default {
    components: {
        FariList,
        FariRowSimple,
        FariRowIcon
    },
    data: function() {
        return {
            currentDir: '/',
            subfolders: null,
            files: null,
            loading: true,
        };
    },
    mounted: function() {
        this.fetchFolderContent();
    },
    activated: function() {
        this.updateHeader();
        this.setDisplayNavigationButtons(false);
    },
    methods: {
        ...mapActions(['setDisplayNavigationButtons']),
        fetchFolderContent: function() {
            fetch('/api/folder-content', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    path: this.currentDir,
                })
            }).then((response) => {
                return response.json();
            }).then((response) => {
                this.subfolders = response.subfolders;
                this.files = response.files;
                this.loading = false;
            })
        },
        openSubfolder: function(path) {
            this.loading = true;
            this.subfolders = null;
            this.files = null;
            if(path == '..') {
                this.currentDir = this.currentDir.split('/').reverse().slice(2).reverse().join('/') + "/";
                if(!this.currentDir) {
                    this.currentDir = "/";
                }
            } else {
                this.currentDir = this.currentDir + path + "/";
            }
            this.fetchFolderContent();
        },
        queueFolder: async function(file) {
            let queue = [];
            let queuePlayIndex = 0;
            for(let i = 0; i < this.files.length; i++) {
                if(this.files[i] == file) {
                    queuePlayIndex = i;
                }
                queue.push({
                    path: this.currentDir + this.files[i]
                });
            }
            await this.$store.dispatch('setQueue', queue);
            await this.$store.dispatch('playFromQueue', queuePlayIndex);
        },
        updateHeader: function() {
            this.$store.dispatch('setHeaderInfo', {
                title: "Folders",
                subtitle: this.currentDir
            });
        }
    },
    watch: {
        currentDir: {
            handler: function(val) {
                this.updateHeader();
            },
            immediate: true
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

</style>
