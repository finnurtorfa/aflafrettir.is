export interface NewsArticle {
  id: string;
  title: string;
  name: string;
  content: string;
  author: string;
  createdAt: string;
  updatedAt: string;
  publishDate: string;
  category: string;
  published: boolean;
}

export interface Ad {
  id: string;
  title: string;
  imageUrl: string;
  linkUrl: string;
  position: string;
  active: boolean;
}

export interface User {
  id: string;
  email: string;
  name: string;
  token: string;
}

export interface FishingReport {
  species: string;
  quantity: number;
  date: string;
  location: string;
}

export interface Category {
  id: string;
  name: string;
  isActive: boolean;
  order: number;
  createdAt: string;
  updatedAt: string;
}
