<template>
<div>
    <div v-if="loading">Loading!</div>
    <div v-else>
        <table>
            <tr v-if="currentDir !== '/'">
                <td><button @click="openSubfolder('..')">&lt;-</button></td>
                <td>..</td>
            </tr>
            <tr v-for="item in subfolders" :key="item">
                <td><button  @click="openSubfolder(item)">open</button></td>
                <td>{{item}}</td>
            </tr>
            <tr v-for="item in files" :key="item">
                <td></td>
                <td>{{item}}</td>
            </tr>
        </table>
    </div>
</div>
</template>

<script>
export default {
    name: 'app',
    data: function() {
        return {
            currentDir: '/',
            subfolders: null,
            files: null,
            loading: true,
        };
    },
    created: function() {
        this.fetchFolderContent();
    },
    methods: {
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
                this.currentDir = this.currentDir.split('/').reverse().slice(1).reverse().join('/');
                if(!this.currentDir) {
                    this.currentDir = "/";
                }
            } else {
                this.currentDir = this.currentDir + path;
            }
            this.fetchFolderContent();
        }
    }
}
</script>

<style lang="scss">
</style>
