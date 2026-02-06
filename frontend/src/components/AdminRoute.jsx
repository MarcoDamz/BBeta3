import { Navigate } from "react-router-dom";
import { useStore } from "../store/useStore";

export default function AdminRoute({ children }) {
  const user = useStore((state) => state.user);

  // Vérifier si l'utilisateur est authentifié
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Vérifier si l'utilisateur a les droits admin
  const isAdmin =
    user.is_admin ||
    user.is_staff ||
    user.is_superuser ||
    (user.groups && user.groups.includes("Administrators"));

  if (!isAdmin) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 flex items-center justify-center p-4">
        <div className="bg-white border border-red-200 rounded-2xl shadow-2xl p-8 max-w-md text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">
            Accès Refusé
          </h1>
          <p className="text-gray-600 mb-6">
            Vous n'avez pas les permissions nécessaires pour accéder à cette
            page.
            <br />
            <span className="text-sm text-gray-500 mt-2 block">
              Seuls les administrateurs peuvent accéder à cette section.
            </span>
          </p>
          <button
            onClick={() => window.history.back()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors font-semibold"
          >
            Retour
          </button>
        </div>
      </div>
    );
  }

  return children;
}
