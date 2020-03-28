<template>
    <FariList>
        <div class="view-wrapper">
            <FariButton @click="onRemakeLibraryClick()">Remake library</FariButton>
            <!-- <FariButton>Remake artists/albums</FariButton> -->
        </div>
    </FariList>
</template>

<script>
import FariList from "@/components/FariList.vue";
import FariButton from "@/components/FariButton.vue";
import { mapGetters, mapActions } from 'vuex';

export default {
    components: {
        FariList,
        FariButton
    },
    data: function() {
        return {
            keyCounter: 0,
        };
    },
    activated: function() {
        this.$store.dispatch('setHeaderInfo', {
            title: "Server",
        });
    },
    computed: {
        ...mapGetters([]),
    },
    methods: {
        ...mapActions(["setLoadingScreen"]),
        onRemakeLibraryClick: function() {
            fetch('/api/remake-library', {
                method: 'GET'
            }).then(async (response) => {
                if(response.status === 200) {
                    console.log(await response.json());
                    window.location.reload();
                } else {
                    console.error(response);
                }
            });
            this.setLoadingScreen(true);
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.view-wrapper {
    color: $text-color;

    @include breakpoint(mobile) {
        display: flex;
        flex-direction: column;
    }

    @include breakpoint(not-mobile) {
        display: grid;
        grid-template-columns: 50% 50%;
    }
}

</style>
