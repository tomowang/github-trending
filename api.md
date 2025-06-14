# GitHub Trending Crawler API

> Version 0.1.0

API to crawl GitHub trending repositories and return structured data.

## Path Table

| Method | Path                                         | Description              |
| ------ | -------------------------------------------- | ------------------------ |
| GET    | [/trending](#gettrending)                    | Get Trending Api         |
| GET    | [/trending/{language}](#gettrendinglanguage) | Get Trending By Language |

## Reference Table

| Name                | Path                                                                              | Description                                     |
| ------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------- |
| HTTPValidationError | [#/components/schemas/HTTPValidationError](#componentsschemashttpvalidationerror) |                                                 |
| TrendingRepository  | [#/components/schemas/TrendingRepository](#componentsschemastrendingrepository)   | Represents a single trending GitHub repository. |
| ValidationError     | [#/components/schemas/ValidationError](#componentsschemasvalidationerror)         |                                                 |

## Path Details

---

### [GET]/trending

- Summary
  Get Trending Api

- Description
  Endpoint to get trending repositories from GitHub.
  Returns a list of structured data for each repository.

#### Responses

- 200 Successful Response

`application/json`

```ts
// Represents a single trending GitHub repository.
{
  name: string
  description?: Partial(string) & Partial(null)
  language?: Partial(string) & Partial(null)
  stars: integer
  forks: integer
  today_stars?: Partial(integer) & Partial(null)
  built_by?: string[]
}[]
```

---

### [GET]/trending/{language}

- Summary
  Get Trending By Language

- Description
  Endpoint to get trending repositories from GitHub by language.
  Returns a list of structured data for each repository.

#### Responses

- 200 Successful Response

`application/json`

```ts
// Represents a single trending GitHub repository.
{
  name: string
  description?: Partial(string) & Partial(null)
  language?: Partial(string) & Partial(null)
  stars: integer
  forks: integer
  today_stars?: Partial(integer) & Partial(null)
  built_by?: string[]
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

## References

### #/components/schemas/HTTPValidationError

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

### #/components/schemas/TrendingRepository

```ts
// Represents a single trending GitHub repository.
{
  name: string
  description?: Partial(string) & Partial(null)
  language?: Partial(string) & Partial(null)
  stars: integer
  forks: integer
  today_stars?: Partial(integer) & Partial(null)
  built_by?: string[]
}
```

### #/components/schemas/ValidationError

```ts
{
  loc?: Partial(string) & Partial(integer)[]
  msg: string
  type: string
}
```
