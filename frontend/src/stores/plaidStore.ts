import { defineStore } from "pinia";
import { ref } from "vue";
import { financeApi } from "../services/api";
import { useToastStore } from "./toastStore";

export const usePlaidStore = defineStore("plaid", () => {
  const linkToken = ref("");
  const status = ref("Not connected");
  const loading = ref(false);

  async function createLinkToken() {
    loading.value = true;
    try {
      const result = await financeApi.createLinkToken();
      linkToken.value = result.link_token;
      status.value = "Link token created";
      useToastStore().success("Link token created", "The Plaid Sandbox link token is ready.");
    } catch (err) {
      useToastStore().error("Plaid link token failed", err instanceof Error ? err.message : "Check backend Plaid credentials.");
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function exchangePublicToken(publicToken: string) {
    loading.value = true;
    try {
      await financeApi.exchangePublicToken(publicToken);
      status.value = "Sandbox item connected";
      useToastStore().success("Plaid item connected", "Public token was exchanged by the backend.");
    } catch (err) {
      useToastStore().error("Token exchange failed", err instanceof Error ? err.message : "Public token could not be exchanged.");
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function syncTransactions() {
    loading.value = true;
    try {
      await financeApi.syncTransactions();
      status.value = "Transactions synced";
      useToastStore().success("Transactions synced", "Plaid Sandbox transactions were imported.");
    } catch (err) {
      useToastStore().error("Transaction sync failed", err instanceof Error ? err.message : "No Plaid item may be connected.");
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return { linkToken, status, loading, createLinkToken, exchangePublicToken, syncTransactions };
});
