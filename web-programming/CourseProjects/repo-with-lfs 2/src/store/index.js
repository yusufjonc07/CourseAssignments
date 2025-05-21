import { createStore } from "vuex";

export default createStore({
  state: {
    loading: false,
  },
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading;
    },
  },
  actions: {
    setloading({ commit }, loading) {
      commit("SET_LOADING", loading);
    },
  },
  getters: {
    loading(state) {
      return state.loading;
    },
  },
  modules: {},
});
